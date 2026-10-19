# How do aggregators find companies and their ATS slugs?

The ATS APIs work one company at a time ([ats-job-apis.md](ats-job-apis.md)), so an ATS-first aggregator is only as complete as its list of (company, ATS, slug). This is the "company universe" problem. Live checks below marked "(probed 2026-10-19)" were made during research.

## Concepts

- **Slug / board token:** the company's name in the board URL (`jobs.lever.co/{slug}`). The hostname identifies the ATS, and the first path segment (or the subdomain) is the slug ([Apify vellumlabs](https://apify.com/vellumlabs/ats-job-board-finder)).
- **Workday is a triple**, not a slug: tenant, data-centre shard (`wd1`, `wd5`, ...) and site name, e.g. `23andme|wd5|23` ([Feashliaa data](https://github.com/Feashliaa/job-board-aggregator/tree/main/data)).
- **Verification:** all three major APIs return a clean 404 for an unknown slug. Greenhouse returns `{"status":404,...}`, Lever `{"ok":false,...}`, Ashby plain "Not Found" (probed 2026-10-19) ([Greenhouse](https://boards-api.greenhouse.io/v1/boards/zzqqnotreal123/jobs); [Lever](https://api.lever.co/v0/postings/zzqqnotreal123?mode=json); [Ashby](https://api.ashbyhq.com/posting-api/job-board/zzqqnotreal123)). So the public API is the natural gate for whether a candidate is real. *(synthesis)*

## Three ways a company–ATS pair is found

| Method | What it yields | Strength | Weakness |
|---|---|---|---|
| Careers-page inspection | Links or embeds pointing at hosted boards, from a few pages of the company site ([vellumlabs](https://apify.com/vellumlabs/ats-job-board-finder)) | Catches slugs that don't match the company name | Needs the company domain first. Misses custom embeds and white-label domains |
| Slug guessing | Name variants ("huggingface", "hugging-face") tested against each ATS ([vellumlabs](https://apify.com/vellumlabs/ats-job-board-finder)) | Cheap | False positives (a different company with the same slug), so guessed hits get flagged for review |
| Index mining | ATS hostnames found in crawl or search indexes, with slugs pulled out of the URLs ([Feashliaa](https://github.com/Feashliaa/job-board-aggregator)) | Yields slugs directly, at scale | Only boards that got crawled. Includes dead slugs |

Hostname matching is cheap and reliable for hosted boards. The hard cases are custom-domain career sites and Workday's triple. *(synthesis)*

## Seed sources

**Crawl and search indexes**
- **Common Crawl** has a CDX server and a Parquet columnar index (about 300 GB per monthly crawl, queried with Athena) ([Common Crawl](https://commoncrawl.org/blog/index-to-warc-files-and-urls-in-columnar-format)). The public CDX server returned HTTP 504 for every ATS-hostname query tried on 2026-10-19 ([CDX](https://index.commoncrawl.org/CC-MAIN-2026-39-index?url=jobs.ashbyhq.com/*&showNumPages=true)), so bulk work runs on the columnar index.
- **Wayback Machine and certificate-transparency logs** are used by careerscout ([careerscout](https://github.com/Ramcharan747/careerscout)).
- **Search `site:` queries:** HiringCafe's founder started with `"job openings" site:greenhouse.io` ([HiringCafe blog](https://blog.hiring.cafe/p/scaling-hiringcafe-from-0-to-1m-users)). One project uses SerpApi for a monthly rediscovery ([YvetteZheng0812](https://github.com/YvetteZheng0812/ats-job-scraper)).

**Company databases (they yield domains, not ATS)**
- **People Data Labs Free Company Dataset:** 22M+ companies, CC BY 4.0 ("You may use this data for any purpose"), updated quarterly ([PDL docs](https://docs.peopledatalabs.com/docs/free-company-dataset.md)).
- **YC directory via yc-oss/api** (unofficial, updated daily): 6,307 companies, 1,494 flagged hiring (2026-10-19). There is no ATS field ([yc-oss](https://github.com/yc-oss/api); [hiring.json](https://yc-oss.github.io/api/companies/hiring.json)).
- **Apollo.io** was reportedly the seed for HiringCafe's crawl ([gist](https://gist.github.com/thoroc/21601e286d9d4fec8505a88d71145ad9)).

**Technographic vendors (lists of companies using an ATS)**
- TheirStack: e.g. 1,655 companies using Ashby (undated) ([TheirStack](https://theirstack.com/de/technology/ashby)).
- Bloomberry: per-ATS company lists ([Bloomberry](https://bloomberry.com/data/ashby)).
- jobspipe.dev: lists "checked against the ATS's own public endpoints" (Jul 2026, no counts) ([jobspipe](https://jobspipe.dev/companies-using.md)).

**Open GitHub slug lists**

| Repo | Method | Size | Licence / notes |
|---|---|---|---|
| [Feashliaa/job-board-aggregator](https://github.com/Feashliaa/job-board-aggregator) | Common Crawl CDX, 20+ ATS patterns, deduped across snapshots | Greenhouse 8,333; Workday 12,884; Lever 4,368; Ashby 3,161 (2026-10-19), plus other ATS files. README claims ~95,000 | **Data is CC BY-NC 4.0: commercial use needs permission.** Also appears as Riley-Dorrington/job-board-aggregator (relationship unverified) |
| [rishilahoti/ashby-job-scraper](https://github.com/rishilahoti/ashby-job-scraper) | Daily CDX scan plus live API verification | "2,000+ companies" | Slugs in a DB, not a file |
| [Ramcharan747/careerscout](https://github.com/Ramcharan747/careerscout) | 5.5M domains, slug probing, CDX, Wayback, CT logs | ~930k career pages; 2,100+ ATS sources confirmed; 155 Workday boards | 6 stars |
| [YvetteZheng0812/ats-job-scraper](https://github.com/YvetteZheng0812/ats-job-scraper) | SerpApi search | Small, user-local | Example file only |
| [jshchnz/claude-jobs](https://github.com/jshchnz/claude-jobs) | Hand-curated table in a Claude skill | Small | — |
| [noble-ronin/ats-job-apis](https://github.com/noble-ronin/ats-job-apis) | Endpoint docs for 9 ATS | n/a | Reference, not a list |

### Rules of thumb *(synthesis)*

- Crawl-index mining gives slugs cheaply. Company databases give the universe of companies but need a crawl per domain to resolve the ATS. The bigger projects combine both: the index for slugs, and PDL or YC to see who is missing.
- **For the ad-hoc skill:** a static seed (YC `hiring.json` plus a mined slug list) plus checking a company's careers page on demand is enough. Mind the licence: a CC BY-NC list is fine for personal research but not for a commercial site without permission.
- **For the website:** scheduled re-mining plus re-verification is required.
- careerscout's low yield from 5.5M domains suggests that starting from domains finds fewer boards than crawl-index mining.

## How existing aggregators describe discovery

- **HiringCafe** (Ali Mir, 2025-09-17): "all of our jobs are scraped directly from employers' career page sites". It was seeded from a spreadsheet of "hundreds of employer websites" plus `site:` searches, and uses LLM structured outputs for extraction. 1.3M+ monthly users ([HiringCafe blog](https://blog.hiring.cafe/p/scaling-hiringcafe-from-0-to-1m-users)).
- An unattributed gist describes the build:
  - Apollo for company URLs, then an LLM to classify career pages.
  - Manual review of "the 30,000 company career pages", excluding recruiting firms.
  - Each company crawled 3 times a day.
  - Embeddings to detect reposts.
  - It may be a copy of someone else's write-up ([gist](https://gist.github.com/thoroc/21601e286d9d4fec8505a88d71145ad9)).
- HiringCafe's edge is breadth from crawling career pages directly, not ATS-API-only polling. An ATS-API-only aggregator will miss companies on custom or enterprise career sites. *(synthesis)*
- **Commercial index claims (vendor claims):**
  - About 390,000 jobs from 17,000+ companies, rebuilt twice a day ([Apify JTPalms](https://apify.com/JTPalms/ats-jobs-index)).
  - 25,000+ verified-live boards and 1.4M jobs across four ATS ([Apify zon4a](https://apify.com/zon4a/ats-jobs-api)).
  - "none of [the ATS vendors] publishes a directory of its customers" ([Apify groundtruth](https://apify.com/groundtruth/ats-job-listings)).
- Feashliaa claims 1,000,000+ positions from 20,000+ companies across 7 ATS, refreshed daily ([README](https://github.com/Feashliaa/job-board-aggregator)).

## How lists rot

- **Host moves:** `boards.greenhouse.io/airbnb` now 301-redirects to `job-boards.greenhouse.io/airbnb`, while the API host is unchanged (probed 2026-10-19) ([Greenhouse](https://boards.greenhouse.io/airbnb)). Old and new crawl snapshots therefore show different hosts for the same board.
- **Several boards per company:** Lever suffix variants like `10up-2`, and several Workday sites per tenant ([Feashliaa data](https://github.com/Feashliaa/job-board-aggregator/tree/main/data)).
- **Defences in use:**
  - Dedup across snapshots, pruning jobs older than 30 days, and per-platform volume anomaly checks ([Feashliaa](https://github.com/Feashliaa/job-board-aggregator)).
  - Verifying before adding, and content hashing for changes ([rishilahoti](https://github.com/rishilahoti/ashby-job-scraper)).
- **404 vs empty board:** a 404 means a dead slug. An empty 200 may be a company that migrated and left a dormant board. Only re-checking the careers page catches an ATS switch. Mapping subsidiaries to parents (one Workday tenant hosting several brands) is unsolved in the open projects reviewed. *(synthesis)*
- No source measures churn, i.e. how many slugs die per month.

## Scale

- No census exists. Mined lists hold thousands to tens of thousands per ATS. The largest open claim is about 95k identifiers across 20+ ATS ([Feashliaa](https://github.com/Feashliaa/job-board-aggregator)).
- Counts differ by method: TheirStack's 1,655 Ashby vs Feashliaa's 3,161. Technographics see the vendor's script on a live site. Crawl mining sees every slug ever crawled, dead ones included. *(synthesis)*

## Disagreements

- **Lever and Common Crawl:** one README says Lever blocks Common Crawl's bot ([rishilahoti](https://github.com/rishilahoti/ashby-job-scraper)). Lever's live robots.txt on 2026-10-19 allowed all agents with `Crawl-delay: 1` ([robots.txt](https://jobs.lever.co/robots.txt)). Ashby's robots.txt disallows `/api/` but not the board pages ([robots.txt](https://jobs.ashbyhq.com/robots.txt)).
- **HiringCafe scale:**
  - "thousands" vs "tens of thousands" of sites ([jobright](https://jobright.ai/blog/hiringcafe-review-2026-features-pros-cons-and-alternatives/)).
  - 30k career pages (gist) vs 125,671 companies (third-party directory).
  - 3.66M vs 5.7M jobs ([scoutify](https://scoutify.com/blog/hiringcafe-review/)).
- **Feashliaa:** about 95k identifiers claimed vs 28,746 in the four main files. Unresolved.
- **Slug case-sensitivity:** Greenhouse and Ashby are case-insensitive and Lever case-sensitive, per one vendor. Not verified ([vellumlabs](https://apify.com/vellumlabs/ats-job-board-finder)).

## Sources

- [Apify vellumlabs ATS finder](https://apify.com/vellumlabs/ats-job-board-finder); [Apify JTPalms](https://apify.com/JTPalms/ats-jobs-index); [Apify zon4a](https://apify.com/zon4a/ats-jobs-api); [Apify groundtruth](https://apify.com/groundtruth/ats-job-listings)
- [Greenhouse API probe](https://boards-api.greenhouse.io/v1/boards/zzqqnotreal123/jobs); [Lever API probe](https://api.lever.co/v0/postings/zzqqnotreal123?mode=json); [Ashby API probe](https://api.ashbyhq.com/posting-api/job-board/zzqqnotreal123); [boards.greenhouse.io/airbnb](https://boards.greenhouse.io/airbnb)
- [Feashliaa/job-board-aggregator](https://github.com/Feashliaa/job-board-aggregator) and [its data](https://github.com/Feashliaa/job-board-aggregator/tree/main/data); [rishilahoti/ashby-job-scraper](https://github.com/rishilahoti/ashby-job-scraper); [Ramcharan747/careerscout](https://github.com/Ramcharan747/careerscout); [YvetteZheng0812/ats-job-scraper](https://github.com/YvetteZheng0812/ats-job-scraper); [jshchnz/claude-jobs](https://github.com/jshchnz/claude-jobs); [noble-ronin/ats-job-apis](https://github.com/noble-ronin/ats-job-apis)
- [Common Crawl columnar index](https://commoncrawl.org/blog/index-to-warc-files-and-urls-in-columnar-format); [CDX endpoint](https://index.commoncrawl.org/CC-MAIN-2026-39-index?url=jobs.ashbyhq.com/*&showNumPages=true)
- [jobs.lever.co/robots.txt](https://jobs.lever.co/robots.txt); [jobs.ashbyhq.com/robots.txt](https://jobs.ashbyhq.com/robots.txt)
- [PDL Free Company Dataset](https://docs.peopledatalabs.com/docs/free-company-dataset.md); [yc-oss/api](https://github.com/yc-oss/api); [hiring.json](https://yc-oss.github.io/api/companies/hiring.json)
- [TheirStack Ashby](https://theirstack.com/de/technology/ashby); [Bloomberry Ashby](https://bloomberry.com/data/ashby); [jobspipe companies-using](https://jobspipe.dev/companies-using.md)
- [HiringCafe blog](https://blog.hiring.cafe/p/scaling-hiringcafe-from-0-to-1m-users); [gist](https://gist.github.com/thoroc/21601e286d9d4fec8505a88d71145ad9); [jobright review](https://jobright.ai/blog/hiringcafe-review-2026-features-pros-cons-and-alternatives/); [scoutify review](https://scoutify.com/blog/hiringcafe-review/)
