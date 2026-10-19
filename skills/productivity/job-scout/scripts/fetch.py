"""Parallel fetchers for job-scout. Standard library only.

  fetch.py boards --out DIR [--title REGEX] KEYWORD...
      Free board APIs and the latest HN "Who is hiring?" thread -> DIR/boards.jsonl
  fetch.py ats --out DIR [--title REGEX] SLUG...
      Greenhouse, Lever and Ashby boards -> DIR/ats.jsonl. A bare slug is tried on all
      three; "gh:x", "lever:x" or "ashby:x" queries one.

Every row has: src, company, id, title, location, pay, posted, url, text (plain, capped).
The full boards are kept, so "is this posting still open?" is a lookup in ats.jsonl.
stdout: rows whose title matches --title, per-source counts and failures, and ATS slugs
spotted in board rows (feed those to `ats`).
"""
import argparse, html, json, os, re, sys, threading, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = 'Mozilla/5.0 (job-scout)'
PER_HOST = 4  # concurrent requests per host; the reference asks for a few per second at most
_sems, _lock = {}, threading.Lock()


def get(url):
    host = urllib.parse.urlsplit(url).netloc
    with _lock:
        sem = _sems.setdefault(host, threading.Semaphore(PER_HOST))
    with sem:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())


def plain(s, cap=20000):  # pay and location fine print often sit at the end
    s = html.unescape(html.unescape(s or ''))  # Greenhouse double-encodes
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s)).strip()[:cap]


def day(v):
    if v in (None, '', 0):
        return ''
    if isinstance(v, (int, float)) or str(v).isdigit():
        v = int(v)
        return time.strftime('%Y-%m-%d', time.gmtime(v / 1000 if v > 1e11 else v))
    return str(v)[:10]


def pay(lo, hi, cur='', per=''):
    if not lo and not hi or str(lo) in ('None', '0') and str(hi) in ('None', '0'):
        return ''
    return f'{lo}-{hi} {cur or ""} {per or ""}'.strip()


def row(src, company, id, title, location, pay_, posted, url, text):
    return dict(src=src, company=str(company or ''), id=str(id), title=plain(title, 300),
                location=str(location or ''), pay=pay_ or '', posted=day(posted), url=url or '',
                text=plain(text))


# ---- boards ---------------------------------------------------------------

def himalayas(kw):
    out = []
    for p in (1, 2, 3):
        for j in get(f'https://himalayas.app/jobs/api/search?q={urllib.parse.quote(kw)}&page={p}')['jobs']:
            out.append(row('himalayas', j['companyName'], j['guid'], j['title'],
                           f"{j.get('locationRestrictions') or 'anywhere'} tz={j.get('timezoneRestrictions')}",
                           pay(j.get('minSalary'), j.get('maxSalary'), j.get('currency'), j.get('salaryPeriod')),
                           j.get('pubDate'), j['applicationLink'], j.get('description')))
    return out


def remotive(kw):
    d = get(f'https://remotive.com/api/remote-jobs?category=software-dev&search={urllib.parse.quote(kw)}')
    return [row('remotive', j['company_name'], j['id'], j['title'], j['candidate_required_location'],
                j.get('salary'), j['publication_date'], j['url'], j.get('description')) for j in d['jobs']]


def remoteok(kw):
    d = get(f'https://remoteok.com/api?tag={urllib.parse.quote(kw)}')[1:]  # [0] is the legal notice
    return [row('remoteok', j.get('company'), j['id'], j.get('position'), j.get('location'),
                pay(j.get('salary_min'), j.get('salary_max'), 'USD', 'year'), j.get('date'),
                j.get('apply_url') or j.get('url'), j.get('description')) for j in d]


def jobicy(kw):
    d = get(f'https://jobicy.com/api/v2/remote-jobs?count=50&tag={urllib.parse.quote(kw)}')
    return [row('jobicy', j['companyName'], j['id'], j['jobTitle'], j.get('jobGeo'),
                pay(j.get('salaryMin'), j.get('salaryMax'), j.get('salaryCurrency'), j.get('salaryPeriod')),
                j.get('pubDate'), j['url'], j.get('jobDescription')) for j in d.get('jobs', [])]


def getonbrd(kw):
    d = get(f'https://www.getonbrd.com/api/v0/search/jobs?query={urllib.parse.quote(kw)}&per_page=100')
    out = []
    for j in d.get('data', []):
        a = j['attributes']
        out.append(row('getonbrd', (a.get('company') or {}).get('data', {}).get('id'), j['id'], a['title'],
                       f"remote={a.get('remote')} {a.get('remote_modality')} countries={a.get('countries')}",
                       pay(a.get('min_salary'), a.get('max_salary'), 'USD', 'month'), a.get('published_at'),
                       j.get('links', {}).get('public_url'), a.get('description')))
    return out


def hn(kw):
    t = get('https://hn.algolia.com/api/v1/search_by_date?tags=story,author_whoishiring&query=hiring')
    story = next(h for h in t['hits'] if 'who is hiring' in h['title'].lower())
    d = get(f"https://hn.algolia.com/api/v1/search?tags=comment,story_{story['objectID']}"
            f"&query={urllib.parse.quote(kw)}&hitsPerPage=100")
    # Free text: the first line is usually "Company | Role | Location | ...".
    return [row('hn', plain(c['comment_text']).split('|')[0].strip()[:80], c['objectID'],
                plain(c['comment_text'], 200), '', '', c['created_at'],
                f"https://news.ycombinator.com/item?id={c['objectID']}", c['comment_text'])
            for c in d['hits']]


BOARDS = dict(himalayas=himalayas, remotive=remotive, remoteok=remoteok, jobicy=jobicy,
              getonbrd=getonbrd, hn=hn)

# ---- ATS ------------------------------------------------------------------


def greenhouse(slug):
    d = get(f'https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true')
    return [row(f'gh:{slug}', slug, j['id'], j['title'], j['location']['name'], '',
                j.get('first_published') or j['updated_at'], j['absolute_url'], j.get('content'))
            for j in d['jobs']]


def lever(slug):
    d = get(f'https://api.lever.co/v0/postings/{slug}?mode=json')
    out = []
    for j in d:
        c, s = j.get('categories') or {}, j.get('salaryRange') or {}
        text = ' '.join([j.get('descriptionPlain') or ''] + [l['content'] for l in j.get('lists', [])]
                        + [j.get('additionalPlain') or ''])
        out.append(row(f'lever:{slug}', slug, j['id'], j['text'],
                       f"{c.get('location')} {j.get('workplaceType')} all={c.get('allLocations')}",
                       pay(s.get('min'), s.get('max'), s.get('currency'), s.get('interval')),
                       j.get('createdAt'), j['hostedUrl'], text))
    return out


def ashby(slug):
    d = get(f'https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true')
    return [row(f'ashby:{slug}', slug, j['id'], j['title'],
                f"{j.get('location')} {j.get('workplaceType')} remote={j.get('isRemote')} "
                f"also={[s.get('location') for s in j.get('secondaryLocations') or []]}",
                (j.get('compensation') or {}).get('compensationTierSummary'), j.get('publishedAt'),
                j['jobUrl'], j.get('descriptionPlain') or j.get('descriptionHtml'))
            for j in d.get('jobs', []) if j.get('isListed') is not False]


ATS = dict(gh=greenhouse, lever=lever, ashby=ashby)
# shortcut: Lever's EU host (api.eu.lever.co) isn't tried; add "lever-eu" here if EU-heavy searches miss boards.
SLUG_RE = re.compile(r'(?:boards|job-boards)(?:\.eu)?\.greenhouse\.io/(?:embed/job_board\?for=)?([\w-]+)'
                     r'|jobs\.lever\.co/([\w.-]+)|jobs\.ashbyhq\.com/([\w.%-]+)', re.I)


def slugs_in(rows):
    found = set()
    for r in rows:
        for m in SLUG_RE.finditer(r['url'] + ' ' + r['text']):
            gh, lv, ab = m.groups()
            found.add(f'gh:{gh}' if gh else f'lever:{lv}' if lv else f'ashby:{urllib.parse.unquote(ab)}')
    return sorted(found)


# ---- main -----------------------------------------------------------------

def run(tasks):
    """tasks: list of (label, fn, arg). Returns rows and {label: count or error}."""
    def one(t):
        label, fn, arg = t
        try:
            return label, fn(arg)
        except Exception as e:  # 404 = no board under that slug; anything else gets reported
            return label, e
    rows, status = [], {}
    with ThreadPoolExecutor(16) as ex:
        for label, res in ex.map(one, tasks):
            if isinstance(res, Exception):
                status[label] = 'no board' if getattr(res, 'code', None) == 404 else f'FAILED {res}'
            else:
                rows += res
                status[label] = len(res)
    return rows, status


def main():
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=['boards', 'ats'])
    p.add_argument('names', nargs='+')
    p.add_argument('--out', required=True)
    p.add_argument('--title', help='regex; only matching titles are printed (all rows are saved)')
    a = p.parse_args()
    os.makedirs(a.out, exist_ok=True)

    if a.mode == 'boards':
        tasks = [(f'{name}:{kw}', fn, kw) for kw in a.names for name, fn in BOARDS.items()]
    else:
        tasks = []
        for n in a.names:
            kind, _, slug = n.rpartition(':')
            tasks += [(f'{k}:{slug}', ATS[k], slug) for k in ([kind] if kind else ATS)]
    rows, status = run(tasks)

    seen, uniq = set(), []
    for r in rows:
        if (r['src'].split(':')[0], r['id']) not in seen:
            seen.add((r['src'].split(':')[0], r['id']))
            uniq.append(r)
    path = os.path.join(a.out, f'{a.mode}.jsonl')
    with open(path, 'w') as f:
        f.writelines(json.dumps(r) + '\n' for r in uniq)

    title = re.compile(a.title, re.I) if a.title else None
    for r in sorted(uniq, key=lambda r: r['posted'], reverse=True):
        if title is None or title.search(r['title']):
            print(' | '.join([r['src'], r['posted'], r['title'], r['company'], r['location'][:100], r['pay'], r['url']]))
    print(f'\n# {len(uniq)} rows saved to {path}', file=sys.stderr)
    if a.mode == 'ats':
        found = sorted(l for l, s in status.items() if isinstance(s, int) and s)
        print('# boards found: ' + ', '.join(f'{l} ({status[l]})' for l in found), file=sys.stderr)
        slugs = {l.split(':', 1)[1] for l in status}
        missing = sorted(s for s in slugs if not any(l.endswith(':' + s) for l in found))
        print('# no board on any ATS: ' + ', '.join(missing), file=sys.stderr)
    else:
        per = {}
        for l, s in status.items():
            if isinstance(s, int):
                per[l.split(':')[0]] = per.get(l.split(':')[0], 0) + s
        print('# rows per source, before dedup: ' + ', '.join(f'{k}={v}' for k, v in per.items()), file=sys.stderr)
        print('# ATS slugs seen (pass to `ats`): ' + ' '.join(slugs_in(uniq)), file=sys.stderr)
    for l, s in status.items():
        if isinstance(s, str) and s.startswith('FAILED'):
            print(f'# {l}: {s}', file=sys.stderr)


if __name__ == '__main__':
    main()
