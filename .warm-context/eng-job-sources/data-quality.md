# How do aggregated job postings go wrong: dedup, freshness, ghost and scam jobs, role classification, normalisation?

## Deduplication

### What the sources say

- **Duplicates are the norm.** Textkernel (a job-data vendor, 8 countries) reports an average ad reposted 2–5 times, and duplicates making up 50–80% of crawled ads depending on country ([Textkernel](https://textkernel.com/newsroom/online-job-postings-have-many-duplicates-but-how-can-you-detect-them-if-they-are-not-exact-copies-of-each-other)). Lightcast removes "up to 80%" ([Lightcast KB](https://kb.lightcast.io/en/articles/6957661-how-does-lightcast-handle-duplicate-postings)).
- **Exact matching fails.** Two ads for the same job shared only 37% of their text fragments (179 of 484 "shingles", overlapping word sequences), because sites restructure, shorten and re-label ads ([Textkernel](https://textkernel.com/newsroom/online-job-postings-have-many-duplicates-but-how-can-you-detect-them-if-they-are-not-exact-copies-of-each-other)).
- **The industry approach:** a cheap candidate-retrieval step (shingles plus MinHash sketches), then a learned same-job classifier, not a single similarity threshold. Company boilerplate is stripped first, because it repeats across unrelated ads from the same company ([Textkernel](https://textkernel.com/newsroom/online-job-postings-have-many-duplicates-but-how-can-you-detect-them-if-they-are-not-exact-copies-of-each-other)).
- **Lightcast's rule:** match normalised title, employer and location over a 60-day window. The first ad seen is the "original" ([Lightcast KB](https://kb.lightcast.io/en/articles/6957661-how-does-lightcast-handle-duplicate-postings)).
- **Clustering pitfall:** grouping by connected components chains unrelated ads together (A~B and B~C makes A~C). One practitioner switched to cliques ([Skeptric MinHash](https://skeptric.com/minhash); [Skeptric cliques](https://skeptric.com/similar-companies)).
- **Short texts hurt shingling.** A patent bins by length and compares with KL divergence ([US 8,099,415](https://patents.google.com/patent/US8099415)).
- **Other work:** CareerBuilder's production detector "Apollo" ([IEEE](https://computer.org/csdl/proceedings-article/icdmw/2017/3800a177/12OmNC17hUn)), and Zhao et al. 2021 on how duplicates distort labour statistics ([DOI](https://unpaywall.org/10.1145%2F3486622.3493928)). Only abstracts were read.
- **Built-in duplicate signals:**
  - Google Jobs' `apply_options` lists the boards carrying a job ([SerpApi](https://serpapi.com/google-jobs-api)).
  - Indeed's `requisitionid` can repeat across postings ([Indeed](https://docs.indeed.com/job-sync-xml/xml-feed)).
  - Himalayas dedupes on `guid` ([Himalayas](https://himalayas.app/api)).

### Three regimes *(synthesis)*

| Regime | Text | Metadata | Decision |
|---|---|---|---|
| Same job syndicated across sites | High overlap, restructured | Differs | Retrieval plus classifier works |
| Repost of the same job with a new ID or date | Near-identical | New date | Same opening or new? A product decision |
| Multi-location posting split into N | Identical | Locations differ | One job or N? A product decision |

Sourcing straight from ATS boards collapses the first regime at the source. LinkUp says it indexes only employer sites to avoid duplicates (an old marketing claim) ([FactSet/LinkUp](https://insight.factset.com/resources/at-a-glance-linkup-raw)). Board-sourced data needs the full pipeline. *(synthesis)*

No primary source was found on matching by canonical apply URL or on embedding-based dedup for job ads. HiringCafe reportedly uses embeddings to detect reposts ([gist](https://gist.github.com/thoroc/21601e286d9d4fec8505a88d71145ad9)).

## Freshness and expiry

- **`validThrough` is optional by design.** "If a job posting never expires, or you do not know when the job will expire, do not include this property." `datePosted` is "the original date that employer posted the job" ([Google](https://developers.google.com/search/docs/appearance/structured-data/job-posting)). Greenhouse doesn't emit `validThrough` at all ([Greenhouse support](https://support.greenhouse.io/hc/en-us/articles/115003185526-Job-post-visibility-on-Google-for-Jobs)).
- **Google's accepted expiry signals:** markup removed, `validThrough` in the past, 404/410, or removal through the Indexing API ([Google](https://developers.google.com/search/docs/appearance/structured-data/job-posting)).
- **Observed liveness is the reliable signal.** Use your own first-seen and last-seen timestamps, and whether the posting is still on the ATS. Treat `datePosted` as untrusted, because reposting resets it. *(synthesis)*
- **A live posting is weak evidence of a real opening.** Revelio found hires per posting fell from 0.75 (2018) to below 0.5 (2023). It names reposting and listings left up with no intent to hire as factors ([Revelio](https://www.reveliolabs.com/blog/job-postings-hiring-gap)).
- Source-side lags are in [aggregator-and-board-apis.md](aggregator-and-board-apis.md): Jobicy keeps 7 days, Remotive is delayed 24h.

## Ghost jobs and scams

**Ghost jobs** are postings with no real, current opening. The estimates measure different things and can't be compared:

| Figure | What it measures | Source |
|---|---|---|
| 18–22% of jobs on Greenhouse per quarter | Platform classification (attributed to 2024 or 2025; primary not reached) | [Fox5](https://www.fox5atlanta.com/news/ghost-jobs-greenhouse-analysis) |
| ~39–40% of hiring managers | Survey: company posted a fake listing in the past year (Resume Builder 2024) | [IBTimes](https://www.ibtimes.co.uk/new-legislation-targets-ghost-job-listings-1816174) |
| ~1 in 3 employers | Survey (Clarify Capital, Jan 2025) | [Interview Guys](https://blog.theinterviewguys.com/ghost-jobs-exposed/) |
| 27.4% of US LinkedIn listings | Crude "older than 30 days" heuristic | [Interview Guys](https://blog.theinterviewguys.com/ghost-jobs-exposed/) |

**The law is moving:**
- **Ontario** (effective 2026-01-01, employers with 25+ staff): postings must say whether a vacancy exists, give pay or a range (spread capped at CAD 50k) and disclose AI in screening. Interviewed candidates must hear the outcome within 45 days ([HR Reporter](https://www.hrreporter.com/chrr-plus/employment-law/is-your-job-vacancy-real-ontario-cracks-down-on-employers-posting-ghost-jobs/386162); [Employment Hero](https://employmenthero.com/en-ca/blog/ontario-job-posting-requirements)).
- **New York S8877** passed both chambers in June 2026 and awaits the governor. It covers employers with 100+ staff **and third-party job sites**. Ads must say whether the role is open now, opens later, or only collects résumés. Fines are $2,500 per publication, doubling every 30 days ([SHRM](https://www.shrm.org/topics-tools/news/talent-acquisition/new-york-law-ghost-job-postings); [Saiber](https://www.saiber.com/insights/publications/2026-06-29-new-york-state-senate-and-assembly-pass-legislation-that-requires-greater-transparency-for-job-postings)).
- **Similar bills:** New Jersey, California, Kentucky ([Bloomberg Law](https://news.bloomberglaw.com/states-of-play/state-job-ad-bills-shift-from-pay-ranges-to-ghost-jobs-ai-use)). None was confirmed as enacted in the US by Oct 2026.

**Scams** are a separate, growing fraud problem:
- FTC losses to job and employment-agency scams rose from $90M (2020) to $501M (2024) ([Insurance Journal](https://www.insurancejournal.com/news/national/2025/03/10/815001.htm)).
- In H1 2025, reports rose 19% year on year, with almost $300M lost ([Fortune](https://dc.fortune.com/2025/11/17/ftc-data-confirms-job-offer-text-scams-more-common-now)).
- Google bans fake jobs and postings whose main purpose is collecting applicant data ([Google](https://developers.google.com/search/docs/appearance/structured-data/job-posting)).

**Signals** *(synthesis, from the definitions above)*:
- **Ghost:** long age since first seen; repeated reposting of identical text; explicit talent-pool language; pay missing where the law requires it.
- **Scam:** contact moved off-platform; requests for payment or equipment purchases; no verifiable employer.
- Verified ATS company boards remove most fabricated-employer scams. Board and aggregator data does not.

## Classifying engineering and tech roles

- **US taxonomy (SOC 2018):**
  - 15-1200 Computer Occupations, including 15-1252 Software Developers, 15-1253 QA and 15-1254 Web Developers.
  - 15-2050 Data Scientists.
  - 17-2000 Engineers, including 17-2060 Computer Hardware.
  - 17-3000 Technicians.
  - [BLS SOC 2018](https://www.bls.gov/soc/2018/major_groups.htm). O*NET-SOC 2019 is the current O*NET taxonomy ([O*NET](https://services.onetcenter.org/reference/taxonomy)).
- **International:** ISCO-08, with ESCO as the EU's multilingual extension ([Lightcast KB](https://kb.lightcast.io/en/collections/4026359-occupation-taxonomies)). Crosswalks exist but don't map 1:1 ([iscoCrosswalks](https://repo.miserver.it.umich.edu/cran/web/packages/iscoCrosswalks/vignettes/isco-crosswalks.html)). The ISCO group names were not retrieved (the ILO page returned 403).
- **Accuracy ceilings:**

| System | Accuracy | Source |
|---|---|---|
| BERT ensemble on Indeed ads, UK SOC | ~61% at tier 4, ~72% at tier 3 | [arXiv 2511.23057](https://arxiv.org/abs/2511.23057) |
| Cedefop/ESCO pipeline | 73.8% overall | [Cedefop](https://www.cedefop.europa.eu/files/2a_3_panagiotis_zervas.pdf) |
| LLMs producing official codes from memory | 80–100% error (unverified preprint) | [arXiv 2608.26924](https://arxiv.org/pdf/2608.26924) |

- Retrieve-then-rerank pipelines beat asking an LLM for exact codes directly ([arXiv 2503.12989](https://arxiv.org/abs/2503.12989)).
- **Rules of thumb** *(synthesis)*:
  - Titles like "Solutions Engineer", "Sales Engineer", "Data Analyst" and "Support Engineer" are ambiguous from the title alone. Classify on title plus description and keep a confidence.
  - Send low-confidence cases to "uncertain" instead of forcing a code.
  - For a worldwide product, ISCO/ESCO is the neutral backbone, with SOC/O*NET as a US overlay.
- Unverified: Sales Engineers' SOC placement (believed 41-9031, in Sales) and Data Analyst's (15-2051 or 15-1211).

## Normalisation

- **Remote has at least three meanings:** remote anywhere, remote within a country or region, and hybrid. Google's `TELECOMMUTE` is for 100%-remote jobs only, and `applicantLocationRequirements` is required when remote work is geo-restricted ([Google](https://developers.google.com/search/docs/appearance/structured-data/job-posting)). Store an onsite/hybrid/remote enum plus eligible countries. "Remote" with no country is the dangerous default worldwide. *(synthesis)*
- **Remote detection methods:** Indeed Hiring Lab checks the location field first, then keywords. Its dictionary changed in Jan 2021, so the series is not homogeneous ([Hiring Lab](https://www.hiringlab.org/2023/06/28/methodology-remote-and-hybrid-jobs)). A language-model classifier trained on about 30k labelled postings reached 99% ([IZA DP 15980](https://docs.iza.org/dp15980.pdf)).
- **Salary:** Google's `baseSalary` is "the actual base salary … provided by the employer (not an estimate)", with min/max and a unit (HOUR to YEAR) ([Google](https://developers.google.com/search/docs/appearance/structured-data/job-posting)). Store min, max, currency and period with a provenance flag (stated vs inferred), and never mix the two. *(synthesis)*
- **Pay transparency laws:**
  - **US:** Washington (2023, 15+ staff, 300+ class actions since June 2024), Vermont (2023), New Jersey and Massachusetts. The total count conflicts: 13 states + DC, 16 states + DC, or 27 jurisdictions. These are vendor blogs ([Coggno](https://coggno.com/blog/pay-transparency-laws-by-state-2026-employer-compliance/); [Beancount](https://beancount.io/blog/2026/07/29/pay-transparency-laws-2026-state-by-state-guide); [Clockspot](https://www.clockspot.com/articles/pay-transparency-laws-by-state)).
  - **EU:** the Pay Transparency Directive deadline of 2026-06-07 passed with most states late. Accounts name Slovakia, Malta and Italy as fully transposed. Germany and Denmark target 2027 ([Littler](https://www.littler.com/news-analysis/asap/did-member-states-meet-deadline-status-implementation-eu-pay-transparency); [Trusaic](https://trusaic.com/blog/eu-pay-transparency-directive/)).
  - Coverage of pay data will be uneven. Missing pay where the law requires it is a quality signal in itself. *(synthesis)*
- Not researched: currency conversion, seniority inference, multilingual postings.

## Disagreements

- **Greenhouse 18–22%:** attributed to 2024 by some outlets and 2025 by others.
- **Resume Builder:** 39% vs 40%.
- **Revelio:** hires per posting 0.75 to <0.5 vs "1.2 to <1" (different definitions).
- **Ontario:** which Working for Workers Act created each rule, and whether a CAD 100k fine exists (blog only).
- **EU:** Sweden transposed vs withheld its bill. Lithuania full vs partial.
- **US pay-transparency jurisdiction count:** 13+DC, 16+DC or 27.

## Sources

- [Textkernel duplicates](https://textkernel.com/newsroom/online-job-postings-have-many-duplicates-but-how-can-you-detect-them-if-they-are-not-exact-copies-of-each-other); [Lightcast KB duplicates](https://kb.lightcast.io/en/articles/6957661-how-does-lightcast-handle-duplicate-postings); [IEEE Apollo](https://computer.org/csdl/proceedings-article/icdmw/2017/3800a177/12OmNC17hUn); [Zhao et al. DOI](https://unpaywall.org/10.1145%2F3486622.3493928); [US 8,099,415](https://patents.google.com/patent/US8099415); [Skeptric MinHash](https://skeptric.com/minhash); [Skeptric cliques](https://skeptric.com/similar-companies); [FactSet/LinkUp](https://insight.factset.com/resources/at-a-glance-linkup-raw); [gist](https://gist.github.com/thoroc/21601e286d9d4fec8505a88d71145ad9)
- [SerpApi](https://serpapi.com/google-jobs-api); [Indeed Job Sync XML](https://docs.indeed.com/job-sync-xml/xml-feed); [Himalayas API](https://himalayas.app/api)
- [Google Search Central: job posting](https://developers.google.com/search/docs/appearance/structured-data/job-posting); [Greenhouse support](https://support.greenhouse.io/hc/en-us/articles/115003185526-Job-post-visibility-on-Google-for-Jobs); [Revelio](https://www.reveliolabs.com/blog/job-postings-hiring-gap)
- [Fox5](https://www.fox5atlanta.com/news/ghost-jobs-greenhouse-analysis); [IBTimes](https://www.ibtimes.co.uk/new-legislation-targets-ghost-job-listings-1816174); [Interview Guys](https://blog.theinterviewguys.com/ghost-jobs-exposed/); [HR Reporter](https://www.hrreporter.com/chrr-plus/employment-law/is-your-job-vacancy-real-ontario-cracks-down-on-employers-posting-ghost-jobs/386162); [Employment Hero](https://employmenthero.com/en-ca/blog/ontario-job-posting-requirements); [SHRM](https://www.shrm.org/topics-tools/news/talent-acquisition/new-york-law-ghost-job-postings); [Saiber](https://www.saiber.com/insights/publications/2026-06-29-new-york-state-senate-and-assembly-pass-legislation-that-requires-greater-transparency-for-job-postings); [Bloomberg Law](https://news.bloomberglaw.com/states-of-play/state-job-ad-bills-shift-from-pay-ranges-to-ghost-jobs-ai-use)
- [Insurance Journal (FTC 2024)](https://www.insurancejournal.com/news/national/2025/03/10/815001.htm); [Fortune (FTC H1 2025)](https://dc.fortune.com/2025/11/17/ftc-data-confirms-job-offer-text-scams-more-common-now)
- [BLS SOC 2018](https://www.bls.gov/soc/2018/major_groups.htm); [O*NET taxonomy](https://services.onetcenter.org/reference/taxonomy); [Lightcast taxonomies](https://kb.lightcast.io/en/collections/4026359-occupation-taxonomies); [iscoCrosswalks](https://repo.miserver.it.umich.edu/cran/web/packages/iscoCrosswalks/vignettes/isco-crosswalks.html); [arXiv 2503.12989](https://arxiv.org/abs/2503.12989); [arXiv 2511.23057](https://arxiv.org/abs/2511.23057); [Cedefop](https://www.cedefop.europa.eu/files/2a_3_panagiotis_zervas.pdf); [arXiv 2608.26924](https://arxiv.org/pdf/2608.26924)
- [Hiring Lab methodology](https://www.hiringlab.org/2023/06/28/methodology-remote-and-hybrid-jobs); [IZA DP 15980](https://docs.iza.org/dp15980.pdf)
- [Coggno](https://coggno.com/blog/pay-transparency-laws-by-state-2026-employer-compliance/); [Beancount](https://beancount.io/blog/2026/07/29/pay-transparency-laws-2026-state-by-state-guide); [Clockspot](https://www.clockspot.com/articles/pay-transparency-laws-by-state); [Littler](https://www.littler.com/news-analysis/asap/did-member-states-meet-deadline-status-implementation-eu-pay-transparency); [Trusaic](https://trusaic.com/blog/eu-pay-transparency-directive/)
