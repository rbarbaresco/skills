# Overview: where engineering and tech job postings come from

Read this first. It gives the mental model; the topic files hold the evidence. Figures carry their dates, and vendor numbers are marked as vendor claims.

## 1. The shape of the domain

**Most tech postings start on an employer's applicant tracking system (ATS)**: the software employers use to post jobs and manage applicants. Boards and aggregators are mostly copies of that original.

- In a 2026 crawl of 573 tech employers, four ATS families covered about 97%: Greenhouse 58.6%, Ashby 20.1%, Lever 10.3%, Workday 8.4% ([ResumeGeni, 2026-10-19](https://resumegeni.com/research/ats-market-share-2026)). The Fortune 500 looks different. Workday holds over 40% and SuccessFactors 12% ([Jobscan, 2026-08-20](https://jobscan.co/blog/fortune-500-use-applicant-tracking-systems/)).
- Greenhouse, Lever and Ashby document free endpoints that need no key and return a company's whole board as JSON ([Greenhouse](https://docs.greenhouse.io/job-board.html); [Lever](https://github.com/lever/postings-api); [Ashby](https://developers.ashbyhq.com/docs/public-job-posting-api)).
- The ATS feeds the boards. Greenhouse posts free to Indeed and Glassdoor ([Greenhouse support](https://support.greenhouse.io/hc/en-us/articles/115002006126-Free-job-posts-on-Glassdoor-and-Indeed)). Glassdoor has taken its job feed from Indeed since about 2021 ([Zoho community](https://help.zoho.com/portal/en/community/topic/depricating-glassdoor-from-zoho-recruit?page=14)). Arbeitnow is built from ATS boards ([Arbeitnow](https://www.arbeitnow.com/blog/job-board-api)).
- Copying is heavy. Lightcast removes "up to 80%" of the ads it collects as duplicates ([Lightcast KB](https://kb.lightcast.io/en/articles/6957661-how-does-lightcast-handle-duplicate-postings)). Textkernel, a job-data vendor, reports 50–80% duplicates depending on country, with an average ad posted 2–5 times ([Textkernel](https://textkernel.com/newsroom/online-job-postings-have-many-duplicates-but-how-can-you-detect-them-if-they-are-not-exact-copies-of-each-other)).

So the ATS page is the canonical, logged-out, most stable link for a posting, and a board link is usually a mirror of it. *(synthesis)*

Probes on 2026-10-19 back this up: Indeed, Glassdoor, ZipRecruiter, SEEK, StepStone and Naukri blocked single plain requests from scripts, while Greenhouse, Lever, Ashby, LinkedIn's guest page, Dice, Built In and Wellfound opened. A person in a browser was not tested ([source-landscape.md](source-landscape.md#do-posting-links-work-logged-out)).

### Layers of the landscape

| Layer | Examples | Role | Read access in 2026 |
|---|---|---|---|
| Employer ATS boards | Greenhouse, Lever, Ashby, Workday, Gupy (Brazil) | Where postings start | Keyless JSON for most startup ATS; undocumented endpoints for enterprise ATS |
| Big general boards | LinkedIn, Indeed (and Glassdoor, now merged into it), ZipRecruiter | Copies plus direct posts; most traffic | No public read API ([aggregator-and-board-apis.md](aggregator-and-board-apis.md)) |
| Tech, remote and regional boards | Wellfound, Welcome to the Jungle, Himalayas, Dice, SEEK, Naukri, Stepstone | Niche copies plus direct posts | Some have free APIs with redistribution rules |
| Meta-aggregators | Adzuna, Jooble, Careerjet | Copies of copies | Free keys, built for showing live search results |
| Public employment services | USAJOBS, EURES, Bundesagentur, France Travail | Government channels | Mixed: official APIs, unofficial keys, open data |
| Community | HN "Who is hiring?", SimplifyJobs GitHub lists | Curated, high-signal | Free, stable links |
| Discovery layers | Google for Jobs, Common Crawl, search APIs | Indexes, not sources | Google for Jobs only through paid search-results (SERP) APIs |

## 2. The hard problem is the company universe

The startup ATS APIs work per company. You must already know the company's board name (its "slug" or token). None of them lets you search across companies ([ats-job-apis.md](ats-job-apis.md)). Fetching postings is the easy part. Knowing which companies exist, which ATS each one uses, and its slug is the hard part. *(synthesis)*

- No ATS vendor publishes its customer list ([Apify groundtruth](https://apify.com/groundtruth/ats-job-listings)). No authoritative census of public boards exists.
- Open lists mined from Common Crawl reach thousands to tens of thousands of companies per ATS. One repo holds Greenhouse 8,333, Workday 12,884, Lever 4,368 and Ashby 3,161 (counted 2026-10-19). That repo's data is **CC BY-NC 4.0**, so commercial use needs permission ([Feashliaa/job-board-aggregator](https://github.com/Feashliaa/job-board-aggregator)).
- Workday is identified by three parts (tenant, data-centre shard, site), not one slug ([Feashliaa data](https://github.com/Feashliaa/job-board-aggregator/tree/main/data)).
- Lists go stale as companies switch ATS, hosts move (Greenhouse's `boards.` to `job-boards.`, probed 2026-10-19) and slugs get renamed ([company-discovery.md](company-discovery.md)).
- HiringCafe, the best-known direct-crawl aggregator, says all its jobs come from employers' career pages. It was seeded from company lists and `site:greenhouse.io` searches ([HiringCafe blog, 2025-09-17](https://blog.hiring.cafe/p/scaling-hiringcafe-from-0-to-1m-users)).

## 3. The legal posture

*Background, not legal advice; see [legal-and-ethics.md](legal-and-ethics.md).* The sources point to one conservative posture. *(synthesis)*

| Principle | Why |
|---|---|
| **Collect only logged out; never create accounts** | In the US, scrapers with accounts lost (hiQ 2022, Proxycurl 2025, ProAPIs 2026). A logged-out scraper won (Meta v. Bright Data, 2024) ([NatLawReview](https://www.natlawreview.com/article/linkedin-s-data-scraping-battle-hiq-labs-ends-proposed-judgment); [Lowenstein](https://www.lowenstein.com/news-insights/publications/client-alerts/meta-v-bright-data-ruling-has-important-implications-for-webscraping-activities-by-investment-advisers-im)) |
| **Store facts plus a short snippet plus a link out**, not full descriptions | Facts (title, company, location, salary, apply URL) are not copyrightable; description text may be. In the EU, the database right weighs harm to the source's investment (*CV-Online v Melons*, 2021, [Husovec](https://husovec.eu/2021/06/cjeu-redefines-sui-generis-database-right/); holding not checked against the judgment) |
| **No recruiter personal data** | Names, emails and phones in postings are personal data under the GDPR and Brazil's LGPD even when public ([Slaughter and May](https://thelens.slaughterandmay.com/post/102nequ/caught-in-the-web-edpb-guidelines-on-scraping-for-generative-ai); [Monitor Mercantil](https://monitormercantil.com.br/data-scraping-e-a-responsabilidade-do-controlador/)) |
| **Honor robots.txt and crawl politely** | robots.txt is "not a form of access authorization" ([RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html)), but honoring it is the norm and a candidate EU opt-out signal. Server load alone revived X's claims against Bright Data ([MediaPost](https://www.mediapost.com/publications/article/401510/x-corp-can-revive-scraping-battle-with-bright-dat.html)) |
| **Read each source's terms** | Remotive and Himalayas ban feeding their jobs into other boards or aggregators ([Remotive](https://remotive.com/remote-jobs/api); [Himalayas](https://himalayas.app/api)). Adzuna requires its logo on every advert and deletion of the data on termination ([Adzuna ToS](https://developer.adzuna.com/docs/terms_of_service)) |

## 4. The main forks

### Fork A: ad-hoc Claude skill vs continuous aggregation site

| | Ad-hoc research skill | Continuous worldwide site |
|---|---|---|
| Volume | Low, per question | Millions of postings per month |
| Fits | Live queries: ATS APIs for named companies, free board APIs, HN, a SERP API's free tier | Scheduled polling of a large slug universe plus dedup, expiry and classification pipelines |
| Licensing pressure | Low: answers to one user, links out | High: redistribution bans, attribution rules, database right |
| Company universe | A static seed list (e.g. the YC `hiring.json` list: 1,494 companies on 2026-10-19, [yc-oss](https://yc-oss.github.io/api/companies/hiring.json)) is enough | Needs scheduled re-mining and re-verification |

*(synthesis, from [company-discovery.md](company-discovery.md) and [big-boards-and-data-vendors.md](big-boards-and-data-vendors.md))*

### Fork B: ATS-first vs board scraping

- **ATS-first:** official or stable keyless endpoints, original apply links, few fabricated employers, and the least legal exposure. It misses companies on custom or enterprise career sites, and boards' direct-only posts. *(synthesis)*
- **Board scraping (LinkedIn, Indeed, Glassdoor):** the widest single pool, but against the boards' user agreements. LinkedIn says every scraper lawsuit it brought ended in a ban on scraping, which is LinkedIn's own claim ([The Record](https://therecord.media/linkedin-sues-data-scraping-company)). Practitioners report heavy throttling and frequent breakage ([JobSpy](https://github.com/speedyapply/JobSpy)).
- **Middle ground:** Google for Jobs through a paid SERP API. It shows the boards carrying each job, which helps dedup ([SerpApi](https://serpapi.com/google-jobs-api)).

### Fork C: build vs buy

- **Buy:** self-serve job-data APIs list at roughly $0.30–$33 per 1,000 jobs. TheirStack starts at $49/month for 1,500 jobs ([TheirStack pricing](https://theirstack.com/en/pricing)). Labour-market data vendors (Lightcast, LinkUp, Revelio) price by sales quote.
- **Build:** the ATS APIs are free, but you pay in slug discovery, adapters for each ATS, dedup and expiry. At list prices, about 10M jobs a month from a vendor is on the order of $10k/month. That is an extrapolation, not a quote ([big-boards-and-data-vendors.md](big-boards-and-data-vendors.md)). *(synthesis)*
- Vendor data that comes from LinkedIn carries LinkedIn's legal exposure into the product. Proxycurl's injunction required it to notify customers ([LinkedIn newsroom](https://news.linkedin.com/2025/LinkedInWinsLegalBattleToProtectMemberData)).

## 5. Data quality is a pipeline, not a field

- **Duplicates:** exact matching fails. Two copies of the same job shared only 37% of their text fragments ([Textkernel](https://textkernel.com/newsroom/online-job-postings-have-many-duplicates-but-how-can-you-detect-them-if-they-are-not-exact-copies-of-each-other)).
- **Freshness:** `validThrough` (the expiry field in job markup) is optional by design ([Google](https://developers.google.com/search/docs/appearance/structured-data/job-posting)), and Greenhouse never sets it ([Greenhouse support](https://support.greenhouse.io/hc/en-us/articles/115003185526-Job-post-visibility-on-Google-for-Jobs)). Liveness has to be watched by re-fetching the posting, and the status code alone doesn't prove a link is dead or alive: a closed Greenhouse link redirects to a 200 board page and a closed Ashby link is a 200 empty shell (observed 2026-10-19, [source-landscape.md](source-landscape.md#do-posting-links-work-logged-out)). *(synthesis)*
- **Ghost jobs** (postings with no real opening): estimates range from 18–22% of Greenhouse postings in a quarter to about 40% of hiring managers in surveys. These measures are not comparable. Ontario now requires vacancy disclosure (2026-01-01), and New York passed a bill in June 2026 ([data-quality.md](data-quality.md)).
- **Role classification:** even research systems reach only about 60–75% accuracy at detailed occupation codes ([arXiv 2511.23057](https://arxiv.org/abs/2511.23057); [Cedefop](https://www.cedefop.europa.eu/files/2a_3_panagiotis_zervas.pdf)).

## 6. Questions worth asking early

- Is the site a search front-end that links out, or a store that republishes? This decides most of the legal and licensing analysis. *(synthesis)*
- Which regions matter most? Brazil needs Gupy, APAC can go through the SEEK family, and China is app-centric ([source-landscape.md](source-landscape.md)). Regional boards, the groups that cross-post one ad, and which feeds robots.txt disallows are in [regional-boards.md](regional-boards.md).
- Is a multi-location posting one job or N? Is a repost a new opening? Neither is an algorithm question ([data-quality.md](data-quality.md)).
- Which sources' terms allow storage and redisplay at all? A policy flag for each source comes before ingestion. *(synthesis)*

## Sources

Linked inline; full lists are at the end of each topic file.
