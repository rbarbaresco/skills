# What does scraping LinkedIn, Indeed and Glassdoor involve, and what does commercial job data cost?

This file covers the risk, the reliability and the cost. It does not cover techniques for getting around anti-bot defences. Many comparison pages here are written by competitors (JobsPipe, PredictLeads, Bright Data, ZoomInfo, apiserpent), so treat their figures as marketing unless the vendor's own page confirms them. All prices are as of 2026.

## LinkedIn

### What the logged-out surface is

- A guest jobs endpoint returns HTML job cards, 25 at a time, without login ([JobsPipe](https://jobspipe.dev/blog/linkedin-job-scraper-python)).
- It throttles hard. Bursts get HTTP 429 (Too Many Requests), reportedly after about 10 pages from one IP (one source) ([Linked API](https://linkedapi.io/guides/linkedin-jobs-scraper)). JobSpy says the 429 "clears within about a minute". It also says most board endpoints cap at about 1,000 jobs per search ([JobSpy](https://github.com/speedyapply/JobSpy)). Full coverage would take many narrow queries, which multiplies request volume. *(synthesis)*
- Some popular open-source LinkedIn libraries say their anonymous mode is no longer maintained ([Linked API](https://linkedapi.io/guides/linkedin-jobs-scraper)).
- Which fields are visible logged out (salary, applicant count, full description) was not verified. A JobSpy issue asking for applicant count suggests that field is not exposed ([JobSpy issues](https://github.com/speedyapply/JobSpy/issues)).

### Enforcement history

| Case | What happened | Pattern |
|---|---|---|
| hiQ v. LinkedIn (2022) | Court held the User Agreement's scraping and fake-profile bans enforceable as a contract. Consent judgment: $500,000, permanent injunction, deletion of data and code ([ZwillGen](https://www.zwillgen.com/alternative-data/hiq-v-linkedin-wrapped-up-web-scraping-lessons-learned/); [MediaPost](https://www.mediapost.com/publications/article/380493/web-scraper-agrees-to-pay-linkedin-500000-destr.html)) | Fake accounts, logged in |
| LinkedIn v. Proxycurl (2025) | Sued Jan 2025. Proxycurl shut down on 2025-07-04 and settled. The injunction required deleting LinkedIn data and notifying customers ([Nubela](https://nubela.co/blog/goodbye-proxycurl/); [Social Media Today](https://www.socialmediatoday.com/news/linkedin-wins-legal-case-data-scrapers-proxycurl/756101/)) | Fake accounts |
| LinkedIn v. ProAPIs (2025–2026) | Filed Oct 2025 (5:25-cv-08393). Alleged "hundreds if not thousands" of new fake accounts a day, with data sold for up to $15K/month ([The Record](https://therecord.media/linkedin-sues-data-scraping-company)). Settled in principle Feb 2026 ([Bloomberg Law](https://news.bloomberglaw.com/artificial-intelligence/linkedin-strikes-deal-to-settle-scraping-battle-with-startup)). Final consent judgment 2026-09-16 (one aggregator only) ([Digital Policy Alert](https://digitalpolicyalert.org/event/43954-us-district-court-issued-final-judgment-in-linkedin-v-proapis-data-scraping-lawsuit)) | Fake accounts |

- LinkedIn says every one of its scraper lawsuits ended in a judgment barring scraping. That is LinkedIn's own claim ([The Record](https://therecord.media/linkedin-sues-data-scraping-company)).
- Automated access breaches the User Agreement whether or not the data is public ([JobsPipe](https://jobspipe.dev/blog/linkedin-job-scraper-python)).
- Every case found involved fake or logged-in accounts. None targeted purely logged-out job-card scraping. That is not the same as permission. Anyone who resells LinkedIn-derived data, whether a vendor or the site itself, inherits the exposure. *(synthesis)* Legal background is in [legal-and-ethics.md](legal-and-ethics.md).

## Indeed, Glassdoor, ZipRecruiter, Google Jobs

| Site | What practitioners report | Source |
|---|---|---|
| Indeed | "the best scraper currently with no rate limiting". Description search returns off-target roles | [JobSpy](https://github.com/speedyapply/JobSpy) |
| Indeed | Cloudflare 403s and Turnstile CAPTCHAs during pagination (vendor blog, secondhand) | [Thunderbit](https://thunderbit.com/ru/blog/best-indeed-scrapers) |
| Glassdoor | Rate limits above about 2 requests a second | [JobSpy](https://github.com/speedyapply/JobSpy) |
| Glassdoor | Scrapers that worked in 2022 now mostly get 403s, tied to the 2025 merger into Indeed; logins moved to Indeed in Feb 2026 (vendor blog) | [Thunderbit](https://thunderbit.com/pt/blog/scrape-glassdoor-with-python) |
| ZipRecruiter | US and Canada only | [JobSpy](https://github.com/speedyapply/JobSpy) |
| Google Jobs | "currently unavailable" in JobSpy; issue open since 2025-06-06 | [JobSpy](https://github.com/speedyapply/JobSpy); [issues](https://github.com/speedyapply/JobSpy/issues) |

- **Disagreement on Indeed:** JobSpy may be using a mobile or GraphQL-style API, while Thunderbit describes the web pages. They may be describing different surfaces. That is an inference, not verified.
- Since the merger, Glassdoor's inventory probably overlaps heavily with Indeed's, so it adds little. *(synthesis)*
- For Google Jobs, the realistic route is a paid SERP API (a service that returns search-engine results as data). See the table below.
- No source names which bot-protection product each site uses.

## Open-source scrapers

- **JobSpy** (python-jobspy) is the de facto multi-board tool. It covers LinkedIn, Indeed, Glassdoor, ZipRecruiter, Bayt, Naukri, BDJobs and HelloWork. It has 4.5k stars and no tagged releases. Google has been broken for over 16 months ([JobSpy](https://github.com/speedyapply/JobSpy)).
- Open issues from Jun–Aug 2026 ask for Wellfound, RemoteOK and career-site support. No maintainer replies were visible ([JobSpy issues](https://github.com/speedyapply/JobSpy/issues)).
- A JS port (jobspy-js) and a headless-browser LinkedIn package exist ([jobspy-js](https://www.mintlify.com/borgius/jobspy-js/job-boards/linkedin); [PyPI](https://www.pypi.org/project/linkedin-jobs-scraper)).
- Each board's internal API breaks without warning. These tools fit ad-hoc research better than a production aggregator. Users asking for ATS sources point to the more stable source class. *(synthesis)*

## Commercial job data

The market splits four ways *(synthesis, from the vendors below)*:
- **Self-serve, per-job APIs:** roughly $0.30–$33 per 1,000 jobs.
- **Sales-led labour-market datasets:** Lightcast, LinkUp, Revelio.
- **Scraping marketplaces:** Bright Data, Apify. These carry LinkedIn exposure.
- **SERP APIs for Google Jobs:** SerpApi.

All coverage figures below are **vendor claims**.

| Provider | Source type | Coverage (vendor claim) | Freshness | Price (2026) | Source |
|---|---|---|---|---|---|
| TheirStack | Career sites, ATS, boards, deduplicated | 225M jobs since 2021, ~305k new/day, 195 countries | Hourly to monthly datasets | 1 credit per job; API $49/mo for 1,500 up to $5,500/mo for 5M; 4 req/s | [TheirStack](https://theirstack.com/en/pricing) |
| Fantastic.jobs | 54 ATS, 175–200k+ career sites; boards incl. LinkedIn (disputed) | ~3M ATS + ~11M board jobs a month | Hourly (claim) | From ~$1/1k; Apify feed $0.80/1k, API $4/1k | [fantastic.jobs](https://fantastic.jobs/article/best-job-posting-apis); [Apify](https://apify.com/fantastic-jobs/career-site-job-listing-api?fpr=data) |
| Coresignal | Public web | 582M postings (possibly stale) | Daily | ~$19.60/1k (Mini) to $0.50/1k (Elite), up to $5k/mo; datasets from ~$1k | [apiserpent](https://apiserpent.com/blog/coresignal-pricing-explained) |
| Techmap (jobdatafeeds) | Boards and company sites | 451M+ since 2020, ~8.2M new/month | Feeds | ~$1/1k or $400/country/mo (conflicting); free tier | [PredictLeads](https://predictleads.com/blog/top-5-job-data-providers/); [JobsPipe](https://jobspipe.dev/blog/job-postings-dataset) |
| PredictLeads | Company websites | 220M+ since 2016, 2.8M companies | — | Not found | [PredictLeads](https://predictleads.com/blog/top-5-job-data-providers/) |
| LinkUp | Employer websites only | 315M+ since 2007 | Nightly | Demo required | [PredictLeads](https://predictleads.com/blog/linkup-alternatives/) |
| Lightcast | 220k+ sites incl. 100+ government | US since 2010 | — | Contact sales | [Bright Data](https://brightdata.com/blog/web-data/best-job-posting-data-providers) |
| Revelio Labs | Employer sites, boards, staffing boards | 5B+ postings | — | Undisclosed | [Bright Data](https://brightdata.com/blog/web-data/best-job-posting-data-providers) |
| Bright Data | Scraped, incl. LinkedIn jobs | — | Subscription | Min $250 per 100k records ($2.50/1k); refresh ~$1,200+ | [apiserpent](https://apiserpent.com/blog/brightdata-linkedin-pricing-explained) |
| Apify actors (LinkedIn jobs) | Community scrapers | Per run | On demand | $0.30–$5/1k, most ~$1/1k | [meka.im](https://apify.com/meka.im/linkedin-jobs-scraper); [crawlworks](https://apify.com/crawlworks/linkedin-job-scraper) |
| SerpApi (Google Jobs) | Google Jobs results | What Google indexes | Live | Free 250/mo; $25/1k; $75/5k; $275/30k; $725/100k searches; no rollover | [SerpApi](https://serpapi.com/blog/breakdown-of-serpapis-subscriptions/) |
| Proxycurl | — | Shut down 2025-07-04 | — | — | [Nubela](https://nubela.co/blog/goodbye-proxycurl/) |

### Rules of thumb

- **ATS-first vendors (TheirStack, Fantastic.jobs, Techmap) carry less legal exposure than LinkedIn-derived feeds**, because they source direct employer postings. *(synthesis)*
- **Scale:** at about $1 per 1,000 jobs, 10M jobs a month costs on the order of $10k a month. That is an extrapolation from list prices, not a quote. *(synthesis)*
- **For the ad-hoc skill,** low-volume pay-per-use options fit best: SerpApi's free or $25 tier, TheirStack's $49 tier, or Fantastic.jobs on Apify. *(synthesis)*
- **Volume-billed scrapers surprise users.** One user reported an Apify LinkedIn run costing far more than expected because of result volume ([issue](https://beta-securitybyobscurity.apify.com/curious_coder/linkedin-jobs-scraper/issues/this-scheduled-run-u-jhrRIMcQlQwMrhjz7)).

## The cost of building your own board scraping

- Practitioners say board-scale scraping needs rotating residential proxy pools ([JobsPipe](https://jobspipe.dev/blog/linkedin-job-scraper-python)). One 2026 review prices Bright Data residential proxies at about $8.40/GB at entry, with 15–35% volume discounts ([syncgtm](https://syncgtm.com/blog/bright-data-review-2026)). This is a single source.
- Proxies plus headless-browser compute plus ongoing breakage make self-scraping boards not much cheaper than vendor data at about $1/1k. *(synthesis)*
- Ethics, not sourced here: residential proxy networks route traffic through consumer devices, so their consent model matters. Using them to get past a site's explicit rate limits weakens a "public data" defence. In hiQ, the court enforced the User Agreement as a contract ([ZwillGen](https://www.zwillgen.com/alternative-data/hiq-v-linkedin-wrapped-up-web-scraping-lessons-learned/)). *(synthesis)*

## Disagreements

- **Indeed:** "no rate limiting" ([JobSpy](https://github.com/speedyapply/JobSpy)) vs Cloudflare 403s ([Thunderbit](https://thunderbit.com/ru/blog/best-indeed-scrapers)).
- **Fantastic.jobs:** ATS-only ([JobFront](https://www.jobfront.com/compare)) vs includes LinkedIn, with a $45/mo entry ([JobsPipe](https://jobspipe.dev/alternatives/fantastic-jobs)).
- **Coresignal plans:** 8 credit tiers ([apiserpent](https://apiserpent.com/blog/coresignal-pricing-explained)) vs Starter/Pro/Premium at $49/$800/$1,500 ([fullenrich](https://fullenrich.com/content/coresignal-pricing)). Probably old vs new.
- **Techmap:** about $1/1k vs $400 per country per month.
- **SerpApi 5k tier:** $75 now vs $50 before ([TrustRadius](https://www.trustradius.com/products/serpapi/reviews)).
- **Proxycurl:** a LinkedIn "win" ([Social Media Today](https://www.socialmediatoday.com/news/linkedin-wins-legal-case-data-scrapers-proxycurl/756101/)) vs a settlement ([Nubela](https://nubela.co/blog/goodbye-proxycurl/)).
- **hiQ settlement date:** 6 vs 7 December 2022.

## Open questions

- No primary LinkedIn documentation on guest-endpoint limits exists. All thresholds are practitioner reports.
- No pricing was found for JobsPikr, Mantiks or PredictLeads.
- Coresignal's 582M figure and its sources were not verified.

## Sources

- [JobsPipe LinkedIn scraper blog](https://jobspipe.dev/blog/linkedin-job-scraper-python); [Linked API guide](https://linkedapi.io/guides/linkedin-jobs-scraper); [JobSpy](https://github.com/speedyapply/JobSpy); [JobSpy issues](https://github.com/speedyapply/JobSpy/issues); [jobspy-js](https://www.mintlify.com/borgius/jobspy-js/job-boards/linkedin); [linkedin-jobs-scraper (PyPI)](https://www.pypi.org/project/linkedin-jobs-scraper)
- [ZwillGen](https://www.zwillgen.com/alternative-data/hiq-v-linkedin-wrapped-up-web-scraping-lessons-learned/); [MediaPost hiQ](https://www.mediapost.com/publications/article/380493/web-scraper-agrees-to-pay-linkedin-500000-destr.html); [Nubela](https://nubela.co/blog/goodbye-proxycurl/); [Social Media Today](https://www.socialmediatoday.com/news/linkedin-wins-legal-case-data-scrapers-proxycurl/756101/); [The Record](https://therecord.media/linkedin-sues-data-scraping-company); [Bloomberg Law](https://news.bloomberglaw.com/artificial-intelligence/linkedin-strikes-deal-to-settle-scraping-battle-with-startup); [Digital Policy Alert](https://digitalpolicyalert.org/event/43954-us-district-court-issued-final-judgment-in-linkedin-v-proapis-data-scraping-lawsuit)
- [Thunderbit Indeed](https://thunderbit.com/ru/blog/best-indeed-scrapers); [Thunderbit Glassdoor](https://thunderbit.com/pt/blog/scrape-glassdoor-with-python)
- [TheirStack pricing](https://theirstack.com/en/pricing); [fantastic.jobs](https://fantastic.jobs/article/best-job-posting-apis); [Apify Fantastic.jobs API](https://apify.com/fantastic-jobs/career-site-job-listing-api?fpr=data); [JobFront](https://www.jobfront.com/compare); [JobsPipe vs Fantastic.jobs](https://jobspipe.dev/alternatives/fantastic-jobs)
- [apiserpent Coresignal](https://apiserpent.com/blog/coresignal-pricing-explained); [fullenrich](https://fullenrich.com/content/coresignal-pricing); [PredictLeads top 5](https://predictleads.com/blog/top-5-job-data-providers/); [PredictLeads LinkUp alternatives](https://predictleads.com/blog/linkup-alternatives/); [JobsPipe datasets](https://jobspipe.dev/blog/job-postings-dataset); [Bright Data providers](https://brightdata.com/blog/web-data/best-job-posting-data-providers)
- [apiserpent Bright Data](https://apiserpent.com/blog/brightdata-linkedin-pricing-explained); [meka.im](https://apify.com/meka.im/linkedin-jobs-scraper); [crawlworks](https://apify.com/crawlworks/linkedin-job-scraper); [Apify cost issue](https://beta-securitybyobscurity.apify.com/curious_coder/linkedin-jobs-scraper/issues/this-scheduled-run-u-jhrRIMcQlQwMrhjz7)
- [SerpApi subscriptions](https://serpapi.com/blog/breakdown-of-serpapis-subscriptions/); [TrustRadius SerpApi](https://www.trustradius.com/products/serpapi/reviews)
- [syncgtm Bright Data review](https://syncgtm.com/blog/bright-data-review-2026)
