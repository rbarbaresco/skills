# Which official or free board, aggregator and government APIs exist, and on what terms?

Covers sources that are not per-company ATS boards. Many items rest on one page fetched on 2026-10-19. Vendor blogs (JobsPipe, Apify, Zuplo) sell alternatives and have a motive to call official APIs dead. Where only they back a claim, the text says so.

## Overview table

| Source | Coverage | Access | Limits | Reuse rules | Status, Oct 2026 |
|---|---|---|---|---|---|
| Adzuna | Multi-country aggregator | Free key | 25/min, 250/day, 2,500/month by default | "Adzuna" label (≥116×23 px) linked on every advert; delete all data on termination; non-publishing commercial use is a 14-day trial | Live ([ToS](https://developer.adzuna.com/docs/terms_of_service)) |
| Jooble | Global aggregator | Key by form | Not published | Not on public page | Live ([Jooble](https://jooble.org/api/about)) |
| Careerjet | Global, by locale | Publisher key, v4 | Not published | End-user IP and user agent required; links are `jobviewtrack.com` redirects | Live ([Careerjet](https://www.careerjet.com/partners/api)) |
| USAJOBS | US federal | Free key | Not on quick-start page | Separate ToS | Live ([USAJOBS](https://developer.usajobs.gov/general/quick-start)) |
| The Muse | Mostly US, curated; "Software Engineering" category | Key optional | 3,600/h with key, 500/h without | Terms page not fetched | Live; base URL moved to `www.themuse.com/api/public` ([The Muse](https://www.themuse.com/developers/api/v2)) |
| Reed.co.uk | UK | Free key | 100 results per call | Not stated | Live ([Reed](https://www.reed.co.uk/developers/jobseeker)) |
| Remotive | Remote | No key | Not stated | Link back and name Remotive; **no resubmission to other boards**; 24h delay | Live ([Remotive](https://remotive.com/remote-jobs/api)) |
| Remote OK | Remote, tech-heavy | No key | Not stated | Followed (not nofollow) link plus naming Remote OK, or access is suspended | Live ([Remote OK](https://remoteok.com/api)) |
| Himalayas | Remote | No key, or free key | Free key 60/min, 10,000/day | Link and name Himalayas; Apply must use `applicationLink`; **no resubmission to other boards or aggregators** | Live ([Himalayas](https://himalayas.app/api)) |
| Jobicy | Remote; engineering filter | No key; paid key $0.01 per new job | Last 7 days only, 3h delay, hourly sync at most | Clickable source link; don't present as your own | Live; v2 plus an MCP server ([Jobicy](https://jobicy.com/jobs-rss-feed)) |
| Arbeitnow | Europe (DE-centric) | No key | Not stated | Not stated | Live; built from ATS feeds ([Arbeitnow](https://www.arbeitnow.com/blog/job-board-api)) |
| Working Nomads | Remote | Public JSON | n/a | No terms in the feed | Live ([feed](https://www.workingnomads.com/api/exposed_jobs/)) |
| We Work Remotely | Remote | RSS | n/a | Not verified | Feed returned 403 to the fetcher |
| Findwork.dev | Dev jobs | Login wall on docs | n/a | n/a | Not verified |
| HN Firebase / Algolia | "Who is hiring?" threads | No key | Firebase: "no rate limit" | n/a | Live ([HackerNews/API](https://github.com/HackerNews/API)) |
| Bundesagentur (DE) | Germany | Shared public header key; **unofficial** | Not documented | Not documented | Works per community projects ([bundesAPI](https://github.com/bundesAPI/jobsuche-api)) |
| France Travail | France | Free account, OAuth | ~1,150 results per query (vendor claim) | Full offer incl. logo (vendor claim) | Live ([data.gouv.fr](https://www.data.gouv.fr/organizations/france-travail/dataservices); [JobsPipe](https://jobspipe.dev/blog/france-travail-api)) |
| Canada Job Bank | Canada | Monthly CSV open data | n/a | Open Government Licence (not verified) | CSV last seen 2025-04 ([open.canada.ca](https://open.canada.ca/data/en/dataset/ea639e28-c0fc-48bf-b5dd-b8899bd43072)) |
| EURES | EU/EEA, 31 countries | No official third-party API | n/a | n/a | Scrapers only ([Apify](https://apify.com/parseforge/eu-eures-jobs-scraper/api)) |
| Workforce Australia | Australia | No official API | n/a | n/a | Scrapers only ([Apify](https://apify.com/jobsapi/workforce-australia-jobs-search-scraper/api)) |
| India NCS | India | Undocumented, encrypted envelope | n/a | n/a | No official API ([Apify](https://apify.com/jobsapi/ncs-jobs-search-scraper)) |
| Brazil SINE | Brazil | "SINE Aberto" dataset | n/a | n/a | Last updated 2021-09-28, stale ([dados.gov.br](https://dados.gov.br/dataset/sine-aberto)) |
| Indeed | — | — | — | — | **Publisher API dead** (2023 or 2024) |
| LinkedIn | — | Partner-only, posting side | — | — | **No third-party read API** |
| Glassdoor | — | Sales-led B2B | — | — | **Public API closed** (2021 or 2022) |
| ZipRecruiter | — | Not found | — | — | Not verified |
| Google Cloud Talent Solution | Search over **your own** jobs | Paid GCP | — | — | Live v4; not a data source ([release notes](https://cloud.google.com/talent-solution/docs/release-notes)) |

## Meta-aggregators: built for live display, not bulk harvest

- **Adzuna:** the default quota (250 calls a day), the logo on each advert and "remove all … data acquired from Adzuna" on termination all point the same way. The licensed use is display under a visible Adzuna brand. Using trial data in aggregate (counts, average salaries) needs written consent ([Adzuna ToS](https://developer.adzuna.com/docs/terms_of_service)). Whether storing a deduplicated catalog is allowed is not clear. *(synthesis)*
- **Careerjet:** requires the visitor's IP and user agent (403 without them) and returns tracking redirects ([Careerjet](https://www.careerjet.com/partners/api)). That points to calls made live for each visitor, and its links are not the employer's original URLs. *(synthesis)*
- **Jooble:** pitched at portals that want to show Jooble results in their own design. Endpoint, limits and fields are not published ([Jooble](https://jooble.org/api/about)).
- **The Muse:** filters by category, level, location and company. 20 per page. A 403 usually means throttling ([The Muse](https://www.themuse.com/developers/api/v2)).
- **Reed:** details include the external application URL. There are no salary fields when the employer hides salary ([Reed](https://www.reed.co.uk/developers/jobseeker)).
- **USAJOBS:** the key goes in an `Authorization-Key` header and your email in `User-Agent`. The IT management category code is 2210 ([USAJOBS](https://developer.usajobs.gov/general/quick-start)).

## Remote boards: free, but often anti-redistribution

- **Remotive** names Jooble, Neuvoo, Google Jobs and LinkedIn as places you may not submit its jobs. It also bans using the jobs to collect signups or emails ([Remotive](https://remotive.com/remote-jobs/api)).
- **Himalayas** bans submitting its jobs "to other job boards or aggregators". Its data refreshes daily, and jobs dedupe on `guid` ([Himalayas](https://himalayas.app/api)).
- **Remote OK** puts its legal text in the first element of the API array: link back "with follow, and without nofollow!" ([Remote OK](https://remoteok.com/api)). Its logo is a registered trademark (secondary) ([Apify](https://apify.com/retrainmap/remoteok-jobs)).
- **Jobicy** has a `/status?ids=` endpoint that reports a job as active, closed or unknown. Its free `url` field points to Jobicy's own page. Only the paid key returns the original ATS URL ([Jobicy](https://jobicy.com/jobs-rss-feed)).
- **Arbeitnow** is built from Greenhouse, SmartRecruiters, Join, Teamtailor, Recruitee and Comeet ([Arbeitnow](https://www.arbeitnow.com/blog/job-board-api)). An aggregator that also polls those ATS directly gets the same jobs twice. *(synthesis)*
- The **Working Nomads** feed includes contractor marketplaces (Lemon.io, Proxify) that are not direct employers ([feed](https://www.workingnomads.com/api/exposed_jobs/)).

These bans conflict directly with a site that aggregates every tech job, though not necessarily with an ad-hoc research skill that links out to one user. Each source needs a policy flag (may ingest, link required, original apply URL available) before anything is stored. *(synthesis)*

## Government services

- **Germany:** the community project says the Bundesagentur "provides no official API". The widely used key `jobboerse-jobsuche` belongs to the agency's own web app ([bundesAPI](https://github.com/bundesAPI/jobsuche-api)). It is a public client ID, not a contract, and can be revoked without notice. *(synthesis)*
- **France Travail:** the "Offres d'emploi" API returns active offers in real time ([data.gouv.fr](https://www.data.gouv.fr/organizations/france-travail/dataservices)). Quota and licence details are vendor-reported, since the official docs need a login ([JobsPipe](https://jobspipe.dev/blog/france-travail-api)).
- **Canada:** Job Bank's XML feeds are *inbound*, for boards posting into Job Bank. Outbound content goes through a "Host our content" request ([Job Bank](https://www.jobbank.gc.ca/network)).
- **EURES:** about 169.7K new postings a month across 31 countries (vendor figure) ([jobdatafeeds](https://jobdatafeeds.com/data/portals/eures)).
- No source quantifies the tech share of any public-service board. It is likely low. *(synthesis)*

## Hacker News

- The Firebase API says "There is currently no rate limit". The monthly threads come from the user `whoishiring`. `/jobstories` holds YC job posts, not the hiring threads ([HackerNews/API](https://github.com/HackerNews/API)).
- Each top-level comment is an unstructured post that has to be parsed. Algolia HN search exists, but its details were not verified ([HN Algolia](https://hn.algolia.com/api)).

## Big platforms: no read APIs

- **Indeed:** the Publisher Job Search API is deprecated. Old keys reportedly stopped working, and the remaining APIs are employer-side and partner-gated ([Apify blog](https://blog.apify.com/scrape-indeed-jobs/); [JobsPipe](https://jobspipe.dev/blog/indeed-api-guide)). Arbeitnow agrees ([Arbeitnow](https://www.arbeitnow.com/blog/job-board-api)). docs.indeed.com returned 403, so this was not confirmed officially.
- **LinkedIn:** its job APIs serve authorised partners who *post* jobs ([LinkedIn developer docs](https://developer.linkedin.com/docs/v1/job-posting/linkedin-job-credits-partner-program); [Microsoft Learn](https://learn.microsoft.com/fr-ch/linkedin/talent/premium-job-posting)). New partnerships are reportedly closed (vendor claim) ([JobsPipe](https://jobspipe.dev/answers/does-linkedin-have-a-jobs-api.md)).
- **Glassdoor:** the public API closed to new applications ([Zuplo](https://zuplo.com/blog/2024/09/30/what-is-glassdoor-api)). Access today is sales-led ([JobsPipe](https://jobspipe.dev/sources/glassdoor.md)).
- **Google CTS:** you load your own jobs into it and search them. Older versions shut down on 2021-10-13 ([release notes](https://cloud.google.com/talent-solution/docs/release-notes)).
- That leaves scraping (against their terms), paid vendors, or being an ATS partner that pushes jobs *in*. See [big-boards-and-data-vendors.md](big-boards-and-data-vendors.md). *(synthesis)*

## Attribution and link quality

| Rule | Sources |
|---|---|
| Ban on feeding other aggregators | Remotive, Himalayas |
| Delete on termination | Adzuna |
| Visual branding required | Adzuna (logo size), Remote OK (followed link) |
| Original apply URL available | Himalayas (`applicationLink`), Reed, Remote OK (`apply_url`), Jobicy (paid only) |
| Tracking or own-page links instead | Careerjet (`jobviewtrack.com`), Jobicy free tier |

Sources: [Adzuna](https://developer.adzuna.com/docs/terms_of_service), [Remotive](https://remotive.com/remote-jobs/api), [Himalayas](https://himalayas.app/api), [Remote OK](https://remoteok.com/api), [Jobicy](https://jobicy.com/jobs-rss-feed), [Careerjet](https://www.careerjet.com/partners/api), [Reed](https://www.reed.co.uk/developers/jobseeker).

## Failure modes

- **Staleness:** Jobicy keeps 7 days, Remotive is delayed 24h, Himalayas refreshes daily, the Canada CSV is monthly, and the Brazil dataset dates from 2021 (sources above).
- **Copies of copies:** Adzuna, Jooble and Careerjet re-list each other and the remote boards. *(synthesis)*
- **Redirect links** hide the employer URL, so they are weak dedup keys. *(synthesis)*

## Disagreements

- **Indeed Publisher API retirement:** 2023 vs 2024, both on JobsPipe pages ([guide](https://jobspipe.dev/blog/indeed-api-guide) vs [source page](https://jobspipe.dev/sources/indeed)).
- **Glassdoor API closure:** 2021 ([Zuplo](https://zuplo.com/blog/2024/09/30/what-is-glassdoor-api)) vs 2022 ([JobsPipe](https://jobspipe.dev/sources/glassdoor.md)).
- **Bundesagentur:** "no official API" ([bundesAPI](https://github.com/bundesAPI/jobsuche-api)), yet the endpoint is the agency's own. "Official" is ambiguous here.

## Sources

- [Adzuna ToS](https://developer.adzuna.com/docs/terms_of_service); [Jooble API](https://jooble.org/api/about); [Careerjet API](https://www.careerjet.com/partners/api)
- [USAJOBS quick start](https://developer.usajobs.gov/general/quick-start); [The Muse API v2](https://www.themuse.com/developers/api/v2); [Reed developers](https://www.reed.co.uk/developers/jobseeker)
- [Remotive API](https://remotive.com/remote-jobs/api); [Remote OK API](https://remoteok.com/api); [Apify Remote OK actor](https://apify.com/retrainmap/remoteok-jobs); [Himalayas API](https://himalayas.app/api); [Jobicy API](https://jobicy.com/jobs-rss-feed); [Arbeitnow](https://www.arbeitnow.com/blog/job-board-api); [Working Nomads feed](https://www.workingnomads.com/api/exposed_jobs/)
- [HackerNews/API](https://github.com/HackerNews/API); [HN Algolia](https://hn.algolia.com/api)
- [bundesAPI/jobsuche-api](https://github.com/bundesAPI/jobsuche-api); [France Travail on data.gouv.fr](https://www.data.gouv.fr/organizations/france-travail/dataservices); [JobsPipe France Travail](https://jobspipe.dev/blog/france-travail-api); [open.canada.ca Job Bank](https://open.canada.ca/data/en/dataset/ea639e28-c0fc-48bf-b5dd-b8899bd43072); [Job Bank network](https://www.jobbank.gc.ca/network)
- [Apify EURES](https://apify.com/parseforge/eu-eures-jobs-scraper/api); [jobdatafeeds EURES](https://jobdatafeeds.com/data/portals/eures); [Apify Workforce Australia](https://apify.com/jobsapi/workforce-australia-jobs-search-scraper/api); [Apify NCS](https://apify.com/jobsapi/ncs-jobs-search-scraper); [dados.gov.br SINE Aberto](https://dados.gov.br/dataset/sine-aberto)
- [Apify Indeed blog](https://blog.apify.com/scrape-indeed-jobs/); [JobsPipe Indeed guide](https://jobspipe.dev/blog/indeed-api-guide); [JobsPipe Indeed source](https://jobspipe.dev/sources/indeed)
- [LinkedIn job posting partner program](https://developer.linkedin.com/docs/v1/job-posting/linkedin-job-credits-partner-program); [Microsoft Learn Premium Job Posting](https://learn.microsoft.com/fr-ch/linkedin/talent/premium-job-posting); [JobsPipe LinkedIn](https://jobspipe.dev/answers/does-linkedin-have-a-jobs-api.md)
- [Zuplo Glassdoor](https://zuplo.com/blog/2024/09/30/what-is-glassdoor-api); [JobsPipe Glassdoor](https://jobspipe.dev/sources/glassdoor.md)
- [Google CTS release notes](https://cloud.google.com/talent-solution/docs/release-notes)
