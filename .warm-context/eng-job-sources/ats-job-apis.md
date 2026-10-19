# Which ATS expose public job feeds, and how?

An ATS (applicant tracking system) is the employer software where most tech postings start. This file covers the read surfaces each ATS exposes, how reliable they are, and who uses which ATS. It describes what exists, not how to build a client.

## Concepts

- **Board token / slug:** the per-company name in a board URL (e.g. `jobs.ashbyhq.com/{name}`). Every ATS API below works one company at a time. None searches across companies ([Greenhouse](https://docs.greenhouse.io/job-board.html); [Lever](https://github.com/lever/postings-api); [Ashby](https://developers.ashbyhq.com/docs/public-job-posting-api)). So the bottleneck is knowing the slugs; see [company-discovery.md](company-discovery.md). *(synthesis)*
- **Documented vs "public in practice":** a vendor-documented public API, versus an undocumented endpoint behind the vendor's own career-site frontend. The second kind answers without auth but is unsupported and can change without notice. *(synthesis)*

## Startup and mid-market ATS

| ATS | Read surface | Auth | Format / paging | Documented by vendor? |
|---|---|---|---|---|
| Greenhouse | `boards-api.greenhouse.io/v1/boards/{token}/jobs` (`content=true` for full text) | None for GET | JSON, whole board, no paging | Yes ([docs](https://docs.greenhouse.io/job-board.html)) |
| Lever | `api.lever.co/v0/postings/{site}`; EU instance at `api.eu.lever.co` | None for read | JSON/HTML/iframe; `skip`/`limit` | Yes ([lever/postings-api](https://github.com/lever/postings-api)) |
| Ashby | `api.ashbyhq.com/posting-api/job-board/{name}` (`includeCompensation=true`) | None shown | JSON, no paging documented | Yes ([docs](https://developers.ashbyhq.com/docs/public-job-posting-api)) |
| SmartRecruiters | `api.smartrecruiters.com/v1/companies/{id}/postings` | None in practice; docs describe key/OAuth | JSON, offset/limit, max 100 | Partly ([docs](https://developers.smartrecruiters.com/docs/posting-api); [Mersetti](https://github.com/Mersetti/ats-job-board-apis)) |
| Workable | Widget endpoint `apply.workable.com/api/v1/widget/accounts/{slug}` | None (widget); full API needs OAuth | JSON | No ([Mersetti](https://github.com/Mersetti/ats-job-board-apis)) |
| Recruitee | `{slug}.recruitee.com/api/offers/` | None | JSON; dates not ISO | Community ([fantastic.jobs](https://fantastic.jobs/article/ats-with-api)) |
| Personio | `{slug}.jobs.personio.de/xml` | None | XML, CDATA HTML | Community ([Mersetti](https://github.com/Mersetti/ats-job-board-apis)) |
| Teamtailor | `{careers-domain}/jobs.rss`, if the tenant turns it on | None | RSS | Community ([fantastic.jobs](https://fantastic.jobs/ats/teamtailor)) |
| Breezy HR | `{slug}.breezy.hr/json` | None | JSON, no descriptions | Community ([Mersetti](https://github.com/Mersetti/ats-job-board-apis)) |
| Rippling | `ats.rippling.com/api/v2/board/{slug}/jobs` | None | JSON, 20/page | Community ([Mersetti](https://github.com/Mersetti/ats-job-board-apis)) |
| BambooHR | Careers widget only; internal JSON changes shape | n/a | n/a | Disputed (see Disagreements) |
| JazzHR | Export feed returns 410 Gone | n/a | n/a | Reported dead ([job-poller](https://github.com/Manojkaipu/job-poller)) |
| Pinpoint, Gem, Dover | Not found | ? | ? | Gap |

### What the three official APIs carry

- **Greenhouse:** "Job Board data is publicly available, so authentication is not required for any GET endpoints." It returns `absolute_url`, `updated_at` and `first_published` (single-job response only). `pay_transparency=true` on a single job adds pay ranges ([Greenhouse docs](https://docs.greenhouse.io/job-board.html)). Gotchas: the description is double-encoded HTML, `absolute_url` may point to the employer's own site, and salary often sits only in the text ([Mersetti](https://github.com/Mersetti/ats-job-board-apis)).
- **Lever:** `hostedUrl`, `applyUrl`, `categories`, `workplaceType`, optional `salaryRange`. Filters are case-sensitive, and there is no full-text search. The only documented limit is on application POSTs (2 per second) ([lever/postings-api](https://github.com/lever/postings-api)). The fetch tool paraphrased the README as saying postings "are public and may be scraped". Check the exact wording before quoting it.
- **Ashby:** `jobUrl`, `applyUrl`, `publishedAt`, `isRemote`, `workplaceType`, and compensation tiers when requested. `isListed: false` means the job is reachable by direct link only ([Ashby docs](https://developers.ashbyhq.com/docs/public-job-posting-api)).
- None of the three documents a read rate limit or API-specific terms. No source guarantees that posting URLs stay stable. Each URL is keyed by a stable ID, though, which suits deep links. *(synthesis)*

## Enterprise ATS

No enterprise vendor documents a public feed for third parties. The 2026 community reports say:

| ATS | Surface reported | Caveats |
|---|---|---|
| Workday | `POST {tenant}.wd{N}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs` | Max page size 20. `total` is right on page 1 but 0 on later pages, so a loop that trusts it can stop early ([DEV glitchbound, 2026-08-02](https://dev.to/glitchbound/workdays-job-api-tells-you-there-are-2000-jobs-then-says-0-on-page-two-2c8e)). Another source says the total caps at 2,000 ([Mersetti](https://github.com/Mersetti/ats-job-board-apis)). The official route, Staffing REST, needs a tenant token ([fantastic.jobs](https://fantastic.jobs/ats/workday)) |
| Oracle Recruiting Cloud | `recruitingCEJobRequisitions` REST resource | Oracle says these endpoints are "for Oracle internal use" ([Oracle docs](https://docs.oracle.com/en/cloud/saas/human-resources/farws/api-recruiting-ce-job-requisitions.html)). Community reports say 21/21 tested sites answered with no session ([jobbot #246](https://github.com/ljofreflor/jobbot/issues/246)) |
| Eightfold | `/api/apply/v2/jobs`; newer sites `/api/pcsx/search` | ([job-poller](https://github.com/Manojkaipu/job-poller)) vs "no public API" ([fantastic.jobs](https://fantastic.jobs/ats/eightfold)) |
| iCIMS | `/api/jobs` on many iCIMS/Jibe sites; classic portal "blocked" | Scraper-vendor source ([Apify parseforge](https://apify.com/parseforge/career-site-jobs-scraper)) |
| SuccessFactors, Taleo, Phenom | Career site only | "Gated, no public job feed" ([JobsPipe, 2026-07-16](https://jobspipe.dev/blog/public-vs-gated-ats-apis)). Classic Taleo needs browser rendering ([Apify](https://apify.com/santamaria-automations/career-site-jobs-scraper)) |
| Jobvite | Has a feed "most customers never enable" | ([JobsPipe](https://jobspipe.dev/blog/public-vs-gated-ats-apis)) |

Workday is the one enterprise system with one consistent JSON shape across tenants and a large share (40%+ of the Fortune 500). That makes it the obvious enterprise target, and also the most fragile one, because the endpoint is undocumented. *(synthesis)*

## Market share

All figures are crawl estimates, not audited data.

| Sample | Greenhouse | Ashby | Lever | Workday | Other | Source |
|---|---|---|---|---|---|---|
| 573 tech employers (2026-10-19 build) | 58.6% | 20.1% | 10.3% | 8.4% | Phenom 0.7%, Eightfold 0.5% | [ResumeGeni](https://resumegeni.com/research/ats-market-share-2026) |
| 2,601 top employers, all sectors | 49.9% | 8.3% | 8.9% | 22.9% | Oracle 3.1%, Phenom 2.4% | [ResumeGeni](https://resumegeni.com/research/ats-market-share-2026) |
| Fortune 500 (2026-08-20) | — | — | — | >40% | SuccessFactors 12%, Taleo declining | [Jobscan](https://jobscan.co/blog/fortune-500-use-applicant-tracking-systems/) |
| 13,130 companies (Jobscan, broad) | 19.0% | — | 15.6% | 17.5% | iCIMS 14.4% | [Jobscan](https://jobscan.co/blog/fortune-500-use-applicant-tracking-systems/) |
| 600+ recruiting teams, agency-heavy | 5.2% | 15.6% | 1.5% | — | — | [Pin](https://www.pin.com/blog/ats-market-share-report/) |

- Ashby is rising fast. It was named in 4.1% of recruiting roles in 2022 and 17.8% of roles started in 2025 ([Pin](https://www.pin.com/blog/ats-market-share-report/)). About 70% of the Forbes AI 50 reportedly use it (secondary) ([HeroHunt](https://www.herohunt.ai/blog/agentic-ats-2026-greenhouse-vs-ashby-vs-workday/)).
- These samples are US-centric and skewed to top employers. Non-US and SMB tech (Personio, Teamtailor, Recruitee, Workable, SmartRecruiters, Gupy) is underrepresented. *(synthesis)*

## Terms and reuse

- No ATS vendor's terms explicitly address third-party aggregation of public boards. The Greenhouse, Lever and Ashby docs carry no API terms ([Greenhouse](https://docs.greenhouse.io/job-board.html); [Lever](https://github.com/lever/postings-api); [Ashby](https://developers.ashbyhq.com/docs/public-job-posting-api)). This is an open gap, not a green light.
- The vendors' general terms and each employer's careers-site terms were not read. The descriptions are the employer's content. *(synthesis)*
- Norms stated by scraper vendors and community guides: respect robots.txt and Crawl-delay, keep to about 2 requests per second per host, cache, identify yourself in the User-Agent, and respect Retry-After ([Apify careersignal](https://apify.com/careersignal/greenhouse-jobs-api); [Mersetti](https://github.com/Mersetti/ats-job-board-apis)).

## Changes 2024–2026

- developers.greenhouse.io now redirects to docs.greenhouse.io. Greenhouse's consent fields are being deprecated ([Greenhouse docs](https://docs.greenhouse.io/job-board.html)).
- Hosted Greenhouse boards moved from `boards.greenhouse.io` to `job-boards.greenhouse.io`. The API host is unchanged (probed 2026-10-19; see [company-discovery.md](company-discovery.md)).
- Lever has been owned by Employ since 2022-08-05 ([JazzHR press release](https://www.jazzhr.com/press-release-lever-joins-employ/)).
- JazzHR's feed reportedly returns 410. Eightfold moved to `/api/pcsx/search` ([job-poller](https://github.com/Manojkaipu/job-poller)).
- No breaking change to the Greenhouse, Lever or Ashby public APIs was found.

## Failure modes

- A Lever slug can miss on the global host and exist on the EU instance ([lever/postings-api](https://github.com/lever/postings-api)). *(synthesis)*
- Lower-plan SmartRecruiters customers reportedly have no public feed ([JobsPipe](https://jobspipe.dev/sources/smartrecruiters)).
- Workday's `total` field misleads paging ([DEV glitchbound](https://dev.to/glitchbound/workdays-job-api-tells-you-there-are-2000-jobs-then-says-0-on-page-two-2c8e)).
- Ashby's unlisted jobs and Greenhouse's "prospect" posts are not real public openings ([Ashby](https://developers.ashbyhq.com/docs/public-job-posting-api); [Greenhouse](https://docs.greenhouse.io/job-board.html)).

## Disagreements

- **Workable, Personio, Teamtailor:** "public" (Mersetti, fantastic.jobs) vs "gated" (JobsPipe). Both can be true: the widget or XML feeds need no key, while the full APIs are gated.
- **Workday:** "publicly accessible JSON" (community) vs "gated, no public feed" ([JobsPipe](https://jobspipe.dev/blog/public-vs-gated-ats-apis)).
- **Oracle and Eightfold:** keyless access (GitHub projects) vs "internal use only" / "no public API" ([Oracle](https://docs.oracle.com/en/cloud/saas/human-resources/farws/api-recruiting-ce-job-requisitions.html); [fantastic.jobs](https://fantastic.jobs/ats/oraclecloud)).
- **BambooHR:** no public endpoint ([JobsPipe](https://jobspipe.dev/sources/bamboohr)) vs public JSON ([Apify careersignal](https://apify.com/careersignal/bamboohr-jobs-api)).
- **Greenhouse rate limit:** "throttles abusive callers" vs "no hard limits". Neither is official ([JobsPipe guide](https://jobspipe.dev/guides/greenhouse-jobs-api); [JobsPipe source](https://jobspipe.dev/sources/greenhouse)).
- **Market share:** Greenhouse at 59%, 19% or 5.2%, depending on how the sample was built.

## Sources

- [Greenhouse Job Board API](https://docs.greenhouse.io/job-board.html)
- [lever/postings-api](https://github.com/lever/postings-api)
- [Ashby public job posting API](https://developers.ashbyhq.com/docs/public-job-posting-api)
- [SmartRecruiters Posting API](https://developers.smartrecruiters.com/docs/posting-api)
- [Mersetti/ats-job-board-apis](https://github.com/Mersetti/ats-job-board-apis)
- [fantastic.jobs ATS with API](https://fantastic.jobs/article/ats-with-api); [fantastic.jobs Teamtailor](https://fantastic.jobs/ats/teamtailor); [Workday](https://fantastic.jobs/ats/workday); [Eightfold](https://fantastic.jobs/ats/eightfold); [Oracle](https://fantastic.jobs/ats/oraclecloud)
- [JobsPipe public vs gated](https://jobspipe.dev/blog/public-vs-gated-ats-apis); [SmartRecruiters](https://jobspipe.dev/sources/smartrecruiters); [BambooHR](https://jobspipe.dev/sources/bamboohr); [Greenhouse guide](https://jobspipe.dev/guides/greenhouse-jobs-api); [Greenhouse source](https://jobspipe.dev/sources/greenhouse)
- [Manojkaipu/job-poller](https://github.com/Manojkaipu/job-poller)
- [DEV glitchbound (Workday paging)](https://dev.to/glitchbound/workdays-job-api-tells-you-there-are-2000-jobs-then-says-0-on-page-two-2c8e)
- [Oracle recruitingCEJobRequisitions](https://docs.oracle.com/en/cloud/saas/human-resources/farws/api-recruiting-ce-job-requisitions.html); [ljofreflor/jobbot #246](https://github.com/ljofreflor/jobbot/issues/246)
- [Apify parseforge](https://apify.com/parseforge/career-site-jobs-scraper); [Apify santamaria](https://apify.com/santamaria-automations/career-site-jobs-scraper); [Apify careersignal Greenhouse](https://apify.com/careersignal/greenhouse-jobs-api); [Apify careersignal BambooHR](https://apify.com/careersignal/bamboohr-jobs-api)
- [ResumeGeni ATS market share 2026](https://resumegeni.com/research/ats-market-share-2026); [Jobscan Fortune 500](https://jobscan.co/blog/fortune-500-use-applicant-tracking-systems/); [Pin](https://www.pin.com/blog/ats-market-share-report/); [HeroHunt](https://www.herohunt.ai/blog/agentic-ats-2026-greenhouse-vs-ashby-vs-workday/)
- [JazzHR press release on Lever/Employ](https://www.jazzhr.com/press-release-lever-joins-employ/)
