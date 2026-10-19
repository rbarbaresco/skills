# Job sources for an ad-hoc engineering search

What works without a login, how to query it, and what to watch for. Endpoints were checked on 2026-10-19. Job sources change fast, so when one fails, say so in the report and move on rather than hunting for a workaround.

Ground rules: read only what a logged-out visitor can see, never create accounts, keep to a few requests per second per host, and honour each source's attribution rule when you link to it (a plain link to the source satisfies all of the ones below for a chat answer).

## Contents

1. Employer ATS boards
2. Telling an open posting from a closed one
3. Free board APIs and feeds
4. Web search recipes
5. Big boards
6. Regional boards
7. Scam and ghost-job signs

## 1. Employer ATS boards

An ATS (applicant tracking system) is the software employers post jobs from. Its board is the original copy of a posting, and its link is the one to report. Every API here works **one company at a time**, by the company's board name ("slug"), which is usually the first path segment of its board URL.

| ATS | Read endpoint (no key) | Notes |
|---|---|---|
| Greenhouse | `https://boards-api.greenhouse.io/v1/boards/{slug}/jobs` (`?content=true` for full text) | Whole board, no paging. `absolute_url` may point to the company's own careers site. Description is double-encoded HTML; salary often only in the text. Hosted boards moved to `job-boards.greenhouse.io` |
| Lever | `https://api.lever.co/v0/postings/{slug}?mode=json` | `skip`/`limit` paging. Has `workplaceType`, `categories.location`, sometimes `salaryRange`. A slug missing here may be on the EU host `api.eu.lever.co` |
| Ashby | `https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true` | `isRemote`, `workplaceType`, `publishedAt`, pay tiers. Skip `isListed: false` jobs |
| SmartRecruiters | `https://api.smartrecruiters.com/v1/companies/{id}/postings` | Offset/limit, max 100 |
| Workable | `https://apply.workable.com/api/v1/widget/accounts/{slug}` | Widget endpoint |
| Recruitee | `https://{slug}.recruitee.com/api/offers/` | |
| Personio | `https://{slug}.jobs.personio.de/xml` | XML; common in DACH |
| Rippling | `https://ats.rippling.com/api/v2/board/{slug}/jobs` | 20 a page |
| Workday | `POST https://{tenant}.wd{N}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs` with a JSON body (`{"searchText": "...", "limit": 20, "offset": 0}`) | Undocumented; page size 20; `total` is only right on page 1. Common at large enterprises |
| Gupy (Brazil) | Career sites at `https://{company}.gupy.io`; postings at `/jobs/{id}` | No public read API. Find postings via web search or `portal.gupy.io` |

An unknown slug returns a clean 404 on Greenhouse, Lever and Ashby, so trying a guessed slug (`hugging-face`, `huggingface`) is cheap. A hit could still be a different company with the same name; check the board's company name.

**Finding companies to query:**
- Startups: the YC directory, `https://yc-oss.github.io/api/companies/hiring.json` (unofficial; has industry, team size, location, no ATS field).
- `site:` searches on ATS hosts (section 4) find companies and postings at once.
- A company's careers page usually links or embeds its ATS board; the hostname gives the ATS and the path gives the slug.

## 2. Telling an open posting from a closed one

The status code alone is not enough:

| Source | Closed or unknown posting looks like |
|---|---|
| Greenhouse | 302 to `?error=true`, then a 200 page of the company's board |
| Ashby | 200 with an empty shell (`"posting":null`) |
| Lever, LinkedIn | Plain 404 |
| Any ATS API | Job ID no longer in the board's JSON (the most reliable check) |

Pages with JSON-LD often carry `validThrough` (an expiry date): seen on LinkedIn, Dice, Built In and Welcome to the Jungle's `app.` host. `datePosted` resets on repost, so treat it as a hint. Median time live in one vendor's 2026 data: Lever 8 days, Ashby and Greenhouse 14, LinkedIn and Indeed 30.

## 3. Free board APIs and feeds

All answered without a key on 2026-10-19.

| Source | Coverage | Query |
|---|---|---|
| Himalayas | Remote, large | `https://himalayas.app/jobs/api/search?q={kw}` (20 a page, `&page=N`). Use its `applicationLink` |
| Remotive | Remote | `https://remotive.com/api/remote-jobs?category=software-dev&search={kw}`. Delayed 24h |
| Remote OK | Remote, tech | `https://remoteok.com/api?tag={kw}`. First array item is the legal notice; skip it |
| Jobicy | Remote, last 7 days | `https://jobicy.com/api/v2/remote-jobs?count=50&tag={kw}` |
| Working Nomads | Remote | `https://www.workingnomads.com/api/exposed_jobs/`. Includes contractor marketplaces, not just employers |
| The Muse | Mostly US | `https://www.themuse.com/api/public/jobs?category=Software%20Engineering&page=N` (also `level`, `location`) |
| Arbeitnow | Europe, Germany-heavy | `https://www.arbeitnow.com/api/job-board-api` (built from ATS boards, so expect duplicates) |
| Get on Board | LATAM, tech | `https://www.getonbrd.com/api/v0/search/jobs?query={kw}` |
| Landing.jobs | Portugal / EU, tech | `https://landing.jobs/api/v1/jobs` (50 a page, has salary) |
| Djinni | Ukraine / remote, tech | RSS `https://djinni.co/jobs/rss/?primary_keyword={kw}` |
| Berlin Startup Jobs | Berlin | RSS `https://berlinstartupjobs.com/engineering/feed/` |
| MyCareersFuture | Singapore | `https://api.mycareersfuture.gov.sg/v2/jobs?search={kw}&limit=20` (salary, expiry date; undocumented) |
| Trampos | Brazil | `https://trampos.co/api/v2/opportunities?page=N` |
| HN "Who is hiring?" | Global, startups | Find the month's thread: `https://hn.algolia.com/api/v1/search_by_date?tags=story,author_whoishiring&query=hiring`. Then search its comments: `https://hn.algolia.com/api/v1/search?tags=comment,story_{id}&query={kw}&hitsPerPage=100`. Posts are free text; check the company's own board for the posting |

Keyed but free (only if the user has a key): Adzuna, Reed (UK), USAJOBS (US federal), Trade Me (NZ), France Travail.

## 4. Web search recipes

- Postings on ATS hosts: `site:job-boards.greenhouse.io "{role}" "{place or remote}"`, and the same with `boards.greenhouse.io`, `jobs.lever.co`, `jobs.ashbyhq.com`, `apply.workable.com`, `jobs.personio.de`, `{company}.gupy.io`, `myworkdayjobs.com`.
- Companies of a kind: "{industry} startups {city} series A", "{country} scale-ups hiring engineers 2026", investor portfolio pages, local startup lists.
- Regional boards: `site:{board domain} "{role}"` for the boards in section 6.
- Always open the result; snippets are often stale.

## 5. Big boards

| Board | Logged-out, scripted access (2026-10-19) |
|---|---|
| LinkedIn | Single posting pages (`/jobs/view/{id}`) open as a guest page; search and repeated access hit walls. Cite a link only if you opened it |
| Indeed, Glassdoor (now part of Indeed), ZipRecruiter | 403 to scripts. No read API |
| Wellfound, Dice, Built In, Welcome to the Jungle (`app.` host) | Posting pages open, with JSON-LD |

Dead or not useful: Stack Overflow Jobs, Hired, Triplebyte, Vettery, talent.io, Monster/CareerBuilder (bankrupt 2025).

## 6. Regional boards

"Open" = posting pages loaded for a script on 2026-10-19; "blocked" = 403 to a script (a person may still see them, so they're useful through web search). Many regional boards copy each other's ads; prefer the employer's link.

| Region | Open, with public posting links | Blocked to scripts / app-only |
|---|---|---|
| Brazil | Gupy career sites, GeekHunter, Trampos, BNE, Programathor (listing) | Catho, InfoJobs and Vagas mostly copy Gupy |
| Spanish-speaking LATAM | Get on Board, Computrabajo | Bumeran, OCC (script-rendered) |
| Western / Central Europe | Landing.jobs (PT), Berlin Startup Jobs, jobs.ch (CH), Jobindex (DK, RSS), Jobs.cz, NoFluffJobs and Just Join IT (PL), Djinni (UA), Arbeitnow, WTTJ `app.` host | StepStone, Totaljobs/CWJobs (UK), Indeed DE |
| UK | Reed (API with key) | Totaljobs, CWJobs |
| India | Cutshort, Hirist (category pages), Wellfound India | Naukri, Instahyre, foundit |
| Japan | Green, Wantedly, BizReach (company names hidden) | |
| Korea | Wanted (`wanted.co.kr/wd/{id}`) | Saramin, JobKorea (script-rendered) |
| Taiwan | Cake | 104 (indexed in search) |
| China | Zhaopin | BOSS Zhipin, 51job (app-centric) |
| SE Asia | MyCareersFuture (SG), Kalibrr (PH/ID, many stale) | Jobstreet/Jobsdb, Glints, ITviec, NodeFlair |
| Middle East | | Bayt, GulfTalent, Naukrigulf |
| Africa | Jobberman (NG/GH) | PNet, Careers24 (ZA), Fuzu |
| Canada | Job Bank | Indeed CA, Workopolis, Jobillico |
| AU / NZ | Trade Me API (NZ, with key) | SEEK, Jora |
| US | Wellfound, Dice, Built In, The Muse, YC Work at a Startup, USAJOBS (key) | Indeed, ZipRecruiter |

Boards in the same group repost the same ad: Redarbor (Computrabajo, InfoJobs BR, Catho, OCC), Jobint (Bumeran and siblings), StepStone (StepStone, Totaljobs, CWJobs, PNet), SEEK (SEEK, Jobstreet, Jobsdb, Jora), Info Edge (Naukri, Naukrigulf, Hirist), Indeed (Glassdoor, SimplyHired, Workopolis).

## 7. Scam and ghost-job signs

- **Scam:** asks for payment or equipment purchases, moves contact to a chat app, offers far above market for little detail, employer can't be found on its own site. A posting on the company's own ATS board rules out most fake employers.
- **Ghost job** (a posting with no real opening): open for months, reposted with identical text, talent-pool wording ("we're always looking for..."), no pay range where the law requires one (several US states, Ontario since 2026-01-01).
- **Remote fine print:** "Remote" often means remote within one country or timezone band. Read the location field and the text before calling a role remote for the user's region.
