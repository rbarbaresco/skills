# What kinds of job sources exist, and which are alive in 2026?

Covers general boards, tech/startup/remote boards, regional boards, community sources, career pages and public employment services. For their APIs, see [aggregator-and-board-apis.md](aggregator-and-board-apis.md) and [ats-job-apis.md](ats-job-apis.md). Regional boards are compared in [regional-boards.md](regional-boards.md).

## Vocabulary

- **ATS (applicant tracking system):** the software an employer uses to post jobs and take applications. Its hosted board is often the original copy of a posting.
- **Board:** a site where employers post jobs, or where jobs are copied in.
- **Aggregator:** a site that collects jobs from other sites.
- **Reverse marketplace:** a site where companies apply to candidates (Hired, Vettery, talent.io). It publishes no public posting URLs.
- **Posting intensity:** how many copies one unique job has across sources (Lightcast's term).

## General boards

| Board | Status, Oct 2026 | Notes |
|---|---|---|
| Indeed | Global giant | "350M+ unique visitors every month" (Indeed's own figure, Apr–Sep 2023) ([sponsor page](https://futureworkseries.com/sponsors/indeed)). Third parties count about 444M *visits* (Mar 2026) ([Exploding Topics](https://analytics.explodingtopics.com/website/indeed.com)). Visits and unique visitors can't be compared |
| Glassdoor | Merged into Indeed | Glassdoor "legally merged into Indeed, Inc. on July 1" (year apparently 2026) ([Reworked](https://www.reworked.co/employee-experience/glassdoor-folds-into-indeed/)). The operational integration was announced Jul 2025 with about 1,300 layoffs ([HR Dive](https://www.hrdive.com/news/layoffs-glassdoor-indeed-ai-integration/752876/)). Indeed-linked login required for "full access" from Apr 20, 2026 ([Job Board Doctor](https://www.jobboarddoctor.com/2026/03/13/indeed-and-glassdoor-turn-the-screws-as-multiple-deadlines-loom/)). Job feed has come from Indeed since about 2021 ([Zoho](https://help.zoho.com/portal/en/community/topic/depricating-glassdoor-from-zoho-recruit?page=14)) |
| LinkedIn | Global giant | 1.3B members (not monthly users) and about 8.2K applications a minute, via a fact-check blog ([meetsona.ai](https://meetsona.ai/blog/linkedin-statistics/)). Single posting pages open logged out (observed 2026-10-19; see [below](#do-posting-links-work-logged-out)). "Easy Apply" needs an account ([linkedinrank](https://linkedinrank.com/blogs/can-i-search-for-jobs-on-linkedin-without-an-account)). A vendor claims some filters stopped working for logged-out visitors ([Apify](https://apify.com/apexweb/linkedin-jobs-guest-scraper)) |
| ZipRecruiter | Alive, US-focused | Q2 2026 revenue $118.1M (+5% YoY), 70,000+ paid employers ([Investing.com](https://www.investing.com/news/company-news/ziprecruiter-q2-2026-slides-revenue-beats-margins-expand-to-12-93CH-4839680)) |
| CareerBuilder + Monster | Bankrupt | Chapter 11 on 2025-06-24 to run an asset sale. JobGet was the first bidder for the boards ([Bloomberg Law](https://news.bloomberglaw.com/bankruptcy-law/careerbuilder-monster-files-for-bankruptcy-plans-asset-sale)). Whether the sale closed was not confirmed |
| SimplyHired | Owned by Recruit (Indeed) since 2016 | ([TechCrunch](https://techcrunch.com/2016/07/01/indeed-owner-recruit-holdings-confirms-acquisition-of-simply-hired)) |
| Google for Jobs | Not a board | Indexes `JobPosting` markup from other sites. It has no consumer API ([Joveo](https://www.joveo.com/google-for-jobs-the-ultimate-guide/)). See [structured-data-and-discovery.md](structured-data-and-discovery.md) |

Glassdoor adds little unique job supply now. Monster and CareerBuilder links in older datasets are unreliable after 2025. *(synthesis)*

## Tech, startup and remote boards

**Dead or absorbed:**
- **Stack Overflow Jobs:** all job features gone by 2022-03-31 ([Dice](https://dice.com/career-advice/stack-overflow-jobs-and-developer-stories-ending-by-march-2022)).
- **Hired:** absorbed into Adecco's LHH on 2024-06-14 ([SIA](https://www.staffingindustry.com/news/global-daily-news/adecco-incorporating-hired-lhh-business)).
- **talent.io:** bankrupt in Mar 2025. The new owner kept the freelance business and wound down permanent hiring ([French Tech Journal](https://www.frenchtechjournal.com/french-tech-wire-great-funding-famine/)).
- **Triplebyte, Vettery:** listed as shut down by the same source.
- **Turing:** pivoted to AI training data ([SiliconANGLE](https://siliconangle.com/2025/03/06/ai-training-data-provider-turing-closes-111m-investment/)).
- **Pragmatic Engineer job board:** closed ([Pragmatic Engineer](https://blog.pragmaticengineer.com/tech-jobs-board/)).

**Alive in Oct 2026:**

| Board | Notes |
|---|---|
| Welcome to the Jungle (absorbed Otta) | Merged Jan 2024, renamed Nov 2024. Job pages at `app.welcometothejungle.com/jobs/<id>` ([WTTJ](https://employers.welcometothejungle.com/candidates/welcome-to-the-jungle)) |
| Wellfound (formerly AngelList Talent) | 27,000+ startups hiring (company claim) ([Wellfound](https://wellfound.com/candidates/overview)). A third-party review says 150K+ tech jobs ([angelinvestorsnetwork](https://angelinvestorsnetwork.com/startups/wellfound-startup-platform-review-2026)) |
| Himalayas | 103,862 remote jobs on 2026-08-25, refreshed daily (secondary) ([anygen](https://www.anygen.io/showcase/himalayas-jobs/index.html)). That size suggests it aggregates *(synthesis)* |
| Remote OK | API returns only about the latest 100 jobs. Salary and the better filters are behind a subscription ([Apify vendor](https://apify.com/norespi/remote-jobs-aggregator); [roamjobs](https://roamjobs.com/guides/getting-hired/best-free-remote-job-boards/)) |
| We Work Remotely | Feed holds about 90 jobs ([Apify vendor](https://apify.com/norespi/remote-jobs-aggregator)) |
| Remotive | Free access disputed: free users see 0.4% of listings ([owlapply](https://owlapply.com/en/blog/30-best-websites-for-remote-job-listings)) vs "free" ([employsome](https://employsome.com/best/job-websites-remote-work/)) |
| Working Nomads | 5,405 live listings (2026 guide) ([trulyremotework](https://trulyremotework.com/blog/best-remote-job-boards-2026/)) |
| Dice, Built In, Levels.fyi Jobs, YC Work at a Startup, Arc.dev | Active per 2026 comparison posts (secondary). Built In is thin outside major US metros. Work at a Startup lists YC companies only ([Underdog.io](https://underdog.io/blog/software-engineer-job-board); [foundrole](https://www.foundrole.com/blog/best-job-boards-for-tech-jobs)) |

The reverse marketplaces largely died in 2022–2025. The open boards that serve a public page for each job survived. *(synthesis)*

## Regional boards (summary; detail in [regional-boards.md](regional-boards.md))

| Region | Main names | Notes |
|---|---|---|
| APAC | SEEK (AU/NZ), Jobstreet (SG/MY/PH/ID), Jobsdb (HK/TH) | Unified on one SEEK platform in Feb 2024 across eight markets, about AUD$180M ([Jobstreet](https://my.jobstreet.com/about/news/article/seek-jobstreet-jobsdb-unify)) |
| China | BOSS Zhipin (Kanzhun) | 70.2M monthly active users in Q2 2026 ([Kanzhun IR](https://ir.zhipin.com/news-releases/news-release-details/kanzhun-limited-announces-second-quarter-2026-financial-results)). App-centric and chat-first, so assume weak web links (unverified) *(synthesis)* |
| India | Naukri (Info Edge) | 106M active resumes (FY25 annual report) ([Info Edge](https://www.infoedge.in/pdfs/Report_filings/InfoEdge_Annual_Report_2025.pdf)). JobSpeak index 3,227 in Jul 2026, with AI/ML leading ([AngelOne](https://www.angelone.in/news/stocks/info-edge-s-naukri-jobspeak-report-white-collar-hiring-up-5-in-july-2026-ai-ml-roles-lead-growth)) |
| Europe | Stepstone Group (stepstone.de, Totaljobs, CWJobs), XING / New Work SE, WTTJ | Stepstone runs about 14–18 portals (scraper-vendor sources) ([Apify](https://apify.com/memo23/stepstone-group-scraper)) |
| Brazil | Gupy (ATS), Catho, InfoJobs, Vagas.com.br | Many large companies post only on Gupy. Vagas and Catho republish Gupy jobs ([philipebrazuca](https://philipebrazuca.com/en/job-search-sites-brazil/); [Vagas](https://www.vagas.com.br/vagas-de-gupy)). For Brazil, Gupy coverage likely matters more than any one board *(synthesis)* |

## Do posting links work logged out?

Each posting URL below was fetched once on 2026-10-19 with a plain GET, no cookies and no login, from a non-browser client (curl from a workstation, or a hosted fetch tool). No headers were changed and nothing was retried. **A person in a normal browser on a residential connection may well see more**: bot-protection services usually let a real browser through after a check a script cannot pass. So "blocked" below means "blocked for scripts", not "blocked for people". All rows are observed 2026-10-19 unless a source is linked.

| Board | Result | Title and description visible? | ID pattern | Closed or unknown link |
|---|---|---|---|---|
| LinkedIn | 200, guest page | Yes; sign-in prompts are overlays in the page | `/jobs/view/<id>`, slug optional | Made-up ID → 404. Free posts close after 30 days ([LinkedIn help](https://www.linkedin.com/help/linkedin/answer/a517777)) |
| Indeed | 403 "Blocked"; 401 via the hosted fetcher | No | `viewjob?jk=<16 hex>` | Closed jobs "removed or shown with reduced visibility" ([Indeed](https://uk.indeed.com/help/employers/articles/unavailable-jobs-on-indeed)) |
| Glassdoor | 403 "Forbidden" | No | `job-listing/…htm?jl=<13 digits>` | Not tested |
| ZipRecruiter | 403 bot challenge | No | `/c/<co>/Job/<title>/-in-<city>?jid=<16 hex>` | Not tested |
| Wellfound | 200 | Yes, JSON-LD with full description | `/jobs/<id>-<slug>` | Not tested |
| Dice | 200 | Yes, JSON-LD | `/job-detail/<UUID>` | Not tested |
| Built In | 200 | Yes; a "Summary Generated by Built In" block sits above the employer text | `/job/<slug>/<id>` | Not tested |
| WTTJ (www host) | 403 | No | `/<lang>/companies/<co>/jobs/<slug>_<city>_<id>` | Not tested |
| WTTJ (`app.` host, ex-Otta) | 200 | Yes, JSON-LD | `/jobs/<8-char id>`; a second ID for the same job | Not tested |
| Himalayas | curl 403 bot challenge; hosted fetcher 200 | Yes via the fetcher | `/companies/<co>/jobs/<slug>`, no numeric ID | Not tested |
| Naukri | Connection dropped at the edge | No | `/job-listings-<slug>-<12 digits>` | Not tested |
| SEEK | 403 | No | `/job/<8 digits>` | Not tested |
| StepStone | 403 "Access Denied" | No | `stellenangebote--<slug>--<id>-inline.html` | Not tested |
| Greenhouse | 200 | Yes | `/<board>/jobs/<id>` | Unknown ID → 302 to `?error=true` → 200 board index |
| Lever | 200 | Yes, JSON-LD | `/<co>/<UUID>` | Unknown ID → 404 |
| Ashby | 200 | Yes for a live job | `/<org>/<UUID>` | Closed job → 200 empty "Jobs" shell, `"posting":null` |

- **The split is board vs ATS.** Most big boards blocked both clients from two networks, while every ATS page and the smaller tech boards opened. That both clients were blocked suggests the boards key on the client, not only the IP. *(synthesis)* No block was a redirect to a login page; all were 403, 401 or a dropped connection.
- **A status code does not prove a link is alive.** Greenhouse turns a dead link into a 302 and then a 200 board page, and Ashby returns 200 with an empty shell. A link checker has to look at the final URL or the page data, not only the status. Lever and LinkedIn return a plain 404. *(synthesis from the rows above)*
- **Some pages expose their expiry date.** JSON-LD `validThrough` was present on LinkedIn (1 of 2 postings), Dice, Built In and WTTJ `app.`, and Himalayas prints "Apply before". That gives an expiry hint without a second request.
- **LinkedIn links are not stable across reposts.** A job reposted after 30 days gets a new URL, per an SAP SuccessFactors note seen only as a search snippet ([SAP](https://userapps.support.sap.com/sap/support/knowledge/en/2787433)).
- **Typical lifespans (vendor claim).** One vendor's dataset (generated 2026-09-09, postings closed in the previous 60 days, measured from its first sighting) gives median days live of Lever 8, Ashby 14, Greenhouse 14, Indeed 30, LinkedIn 30, with LinkedIn and Indeed closures clustering at the 30-day expiry ([jobspipe](https://jobspipe.dev/job-posting-lifespan.md)). Treat as indicative only.
- **Single clicks vs volume.** LinkedIn opened on single requests here; practitioner sources say repeated logged-out access hits CAPTCHAs and auth walls ([Nubela](https://nubela.co/blog/search-linkedin-without-login-anonymously/), low authority). Both can be true. Volume was not tested.
- **Indeed's "expired" label** is read by a third party as "often still open, just not visible on Indeed" ([jobspipe](https://jobspipe.dev/blog/job-closed-or-expired-indeed.md)). Indeed's own page only says closed jobs are removed or shown less ([Indeed](https://uk.indeed.com/help/employers/articles/unavailable-jobs-on-indeed)).

## Community sources

- **HN "Who is hiring?":** monthly threads ran through Oct 2026 ([HN Jul 2026](https://news.ycombinator.com/item?id=48747976)). The thread has shrunk by about a third, from 378–412 posts a month to 232–261. The analyst warns this may reflect the thread rather than hiring ([Solheim](https://www.solheimsolutions.no/notes/hn-who-is-hiring/)). Across 13 threads: 9,194 roles from 3,909 posts ([DEV](https://dev.to/arthur_taken/hn-who-is-hiring-in-2026-a-third-fewer-companies-and-2-job-seekers-for-every-one-470f)).
- **SimplifyJobs GitHub lists:** internship and new-grad lists, scraped hourly from career pages, with about 43–46K and 16–18K stars ([SimplifyJobs](https://github.com/orgs/SimplifyJobs/repositories)). They add curation (sponsorship and closed flags), not new supply. *(synthesis)*

## Career pages vs boards

- No recent study measures what share of tech postings exist only on career sites. The "80% of jobs are never posted" claim traces to 1970s networking lore and a 2016 LinkedIn poll ([resumefast](https://www.resumefast.io/blog/hidden-job-market-data-2026)).
- The best proxy is dedup. Lightcast collects from 220,000+ sites and removes "up to 80%" of ads as duplicates ([Lightcast KB](https://kb.lightcast.io/en/articles/6957661-how-does-lightcast-handle-duplicate-postings)). At the top of that range, an average job has about five copies. That is an upper bound *(synthesis)*.
- A 2026 scrape of 30 career sites (3,141 jobs) found Greenhouse 1,281, Workday 750, Ashby 705 and Lever 228 ([DEV](https://dev.to/tidytools/3141-jobs-from-30-career-sites-which-ats-actually-shows-the-salary-4ep8)).
- Older source-of-hire data: career sites 23.4% vs boards 18.1% of external hires (CareerXroads 2013). Boards gave about 50% of applications vs 35% for career sites (Jobvite 2019) ([Zippia](https://www.zippia.com/advice/job-search-statistics/)).

## Public employment services

- **EURES:** 1.96M–3M vacancies depending on the page, refreshed daily by national services ([EURES](https://europa.eu/eures/portal/jv-se/search?lang=en); [EUR-Lex](https://eur-lex.europa.eu/EN/legal-content/summary/eures-the-eu-s-job-mobility-portal.html)).
- **USAJOBS:** an average of 28,438 open jobs a day. Stable `GetJob/ViewDetails/<id>` URLs and a historic API ([USAJOBS](https://help.usajobs.gov/about)).
- These are reliable logged-out sources but sparse in private-sector tech. Tech share was not measured. *(synthesis)*

## Disagreements

- **Honeypot:** "shut down" ([French Tech Journal](https://www.frenchtechjournal.com/french-tech-wire-great-funding-famine/)) vs "Active" on Crunchbase. The domain refused connections on 2026-10-19.
- **Turing:** still a staffing marketplace vs developer-hire pages now redirecting to its expert network ([secondtalent](https://www.secondtalent.com/alternatives/turing/)).
- **Dice:** "strong signal-to-noise" ([Underdog](https://underdog.io/blog/software-engineer-job-board)) vs "lowest response rate" ([foundrole](https://www.foundrole.com/blog/best-job-boards-for-tech-jobs)).
- **SEEK unification date:** Jan 31, Feb 21 or Feb 29, 2024, depending on the outlet.
- **Glassdoor:** the July 2025 announcement and the "July 1" legal merger are probably two stages, not a conflict.

## Open questions

- How long do posting URLs stay live on each board? Only LinkedIn's free-post rule and one vendor dataset were found (see above).
- What a person in a residential browser sees on the boards that blocked scripts: untested.
- Logged-out viewability of BOSS Zhipin deep pages: untested.

## Sources

- [Indeed sponsor page](https://futureworkseries.com/sponsors/indeed); [Exploding Topics](https://analytics.explodingtopics.com/website/indeed.com)
- [HR Dive](https://www.hrdive.com/news/layoffs-glassdoor-indeed-ai-integration/752876/); [Reworked](https://www.reworked.co/employee-experience/glassdoor-folds-into-indeed/); [Job Board Doctor](https://www.jobboarddoctor.com/2026/03/13/indeed-and-glassdoor-turn-the-screws-as-multiple-deadlines-loom/); [Zoho community](https://help.zoho.com/portal/en/community/topic/depricating-glassdoor-from-zoho-recruit?page=14)
- [meetsona.ai](https://meetsona.ai/blog/linkedin-statistics/); [linkedinrank](https://linkedinrank.com/blogs/can-i-search-for-jobs-on-linkedin-without-an-account); [Apify guest scraper](https://apify.com/apexweb/linkedin-jobs-guest-scraper)
- [Investing.com ZipRecruiter Q2 2026](https://www.investing.com/news/company-news/ziprecruiter-q2-2026-slides-revenue-beats-margins-expand-to-12-93CH-4839680); [Bloomberg Law CareerBuilder+Monster](https://news.bloomberglaw.com/bankruptcy-law/careerbuilder-monster-files-for-bankruptcy-plans-asset-sale); [TechCrunch SimplyHired](https://techcrunch.com/2016/07/01/indeed-owner-recruit-holdings-confirms-acquisition-of-simply-hired); [Joveo](https://www.joveo.com/google-for-jobs-the-ultimate-guide/)
- [Dice](https://dice.com/career-advice/stack-overflow-jobs-and-developer-stories-ending-by-march-2022); [SIA Hired](https://www.staffingindustry.com/news/global-daily-news/adecco-incorporating-hired-lhh-business); [French Tech Journal](https://www.frenchtechjournal.com/french-tech-wire-great-funding-famine/); [SiliconANGLE](https://siliconangle.com/2025/03/06/ai-training-data-provider-turing-closes-111m-investment/); [secondtalent](https://www.secondtalent.com/alternatives/turing/); [Pragmatic Engineer](https://blog.pragmaticengineer.com/tech-jobs-board/)
- [WTTJ](https://employers.welcometothejungle.com/candidates/welcome-to-the-jungle); [Wellfound](https://wellfound.com/candidates/overview); [angelinvestorsnetwork](https://angelinvestorsnetwork.com/startups/wellfound-startup-platform-review-2026); [anygen](https://www.anygen.io/showcase/himalayas-jobs/index.html); [Apify remote aggregator](https://apify.com/norespi/remote-jobs-aggregator); [roamjobs](https://roamjobs.com/guides/getting-hired/best-free-remote-job-boards/); [owlapply](https://owlapply.com/en/blog/30-best-websites-for-remote-job-listings); [employsome](https://employsome.com/best/job-websites-remote-work/); [trulyremotework](https://trulyremotework.com/blog/best-remote-job-boards-2026/); [Underdog.io](https://underdog.io/blog/software-engineer-job-board); [foundrole](https://www.foundrole.com/blog/best-job-boards-for-tech-jobs)
- [Jobstreet](https://my.jobstreet.com/about/news/article/seek-jobstreet-jobsdb-unify); [Kanzhun IR](https://ir.zhipin.com/news-releases/news-release-details/kanzhun-limited-announces-second-quarter-2026-financial-results); [Info Edge AR 2025](https://www.infoedge.in/pdfs/Report_filings/InfoEdge_Annual_Report_2025.pdf); [AngelOne](https://www.angelone.in/news/stocks/info-edge-s-naukri-jobspeak-report-white-collar-hiring-up-5-in-july-2026-ai-ml-roles-lead-growth); [Apify Stepstone](https://apify.com/memo23/stepstone-group-scraper); [philipebrazuca](https://philipebrazuca.com/en/job-search-sites-brazil/); [Vagas](https://www.vagas.com.br/vagas-de-gupy)
- Logged-out links: [LinkedIn help](https://www.linkedin.com/help/linkedin/answer/a517777); [Indeed unavailable jobs](https://uk.indeed.com/help/employers/articles/unavailable-jobs-on-indeed); [SAP note](https://userapps.support.sap.com/sap/support/knowledge/en/2787433); [jobspipe lifespan](https://jobspipe.dev/job-posting-lifespan.md); [jobspipe Indeed expired](https://jobspipe.dev/blog/job-closed-or-expired-indeed.md); [Nubela](https://nubela.co/blog/search-linkedin-without-login-anonymously/)
- [HN Jul 2026](https://news.ycombinator.com/item?id=48747976); [Solheim](https://www.solheimsolutions.no/notes/hn-who-is-hiring/); [DEV HN analysis](https://dev.to/arthur_taken/hn-who-is-hiring-in-2026-a-third-fewer-companies-and-2-job-seekers-for-every-one-470f); [SimplifyJobs](https://github.com/orgs/SimplifyJobs/repositories)
- [resumefast](https://www.resumefast.io/blog/hidden-job-market-data-2026); [Lightcast KB](https://kb.lightcast.io/en/articles/6957661-how-does-lightcast-handle-duplicate-postings); [DEV 30 career sites](https://dev.to/tidytools/3141-jobs-from-30-career-sites-which-ats-actually-shows-the-salary-4ep8); [Zippia](https://www.zippia.com/advice/job-search-statistics/)
- [EURES](https://europa.eu/eures/portal/jv-se/search?lang=en); [EUR-Lex](https://eur-lex.europa.eu/EN/legal-content/summary/eures-the-eu-s-job-mobility-portal.html); [USAJOBS](https://help.usajobs.gov/about)
