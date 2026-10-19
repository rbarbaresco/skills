# How do schema.org JobPosting, Google for Jobs, Common Crawl and search APIs help find postings?

These are discovery layers. They index postings that live elsewhere. None of them is a complete or fresh jobs feed on its own.

## schema.org JobPosting

- **What it is:** a machine-readable description of one job, embedded in the job page, usually as JSON-LD (a script block of JSON) or as microdata (HTML attributes). schema.org is at V30.1 (2026-09-16) ([schema.org](https://schema.org/JobPosting)).
- **Properties that matter to an aggregator:** `title`, `datePosted`, `validThrough`, `hiringOrganization`, `jobLocation`, `jobLocationType`, `applicantLocationRequirements`, `baseSalary`, `identifier`, `directApply`, `employmentType`. `applicantLocationRequirements` says where applicants may apply *from*. It explicitly does not mean citizenship or visa ([schema.org](https://schema.org/JobPosting)).
- **Google's required set:** `title`, `description`, `datePosted`, `hiringOrganization`, `jobLocation`. `jobLocation` may be omitted for fully remote jobs that set `applicantLocationRequirements` (page updated 2026-09-08) ([Google Search Central](https://developers.google.com/search/docs/appearance/structured-data/job-posting)).
- **Google's recommended set:** `baseSalary` (the employer's actual salary, "not an estimate"), `directApply` ("still developing how it uses this"), `employmentType` enum, `identifier`, `jobLocationType=TELECOMMUTE` (100% remote only), `validThrough` (omit if unknown). In beta: education and experience requirements ([Google](https://developers.google.com/search/docs/appearance/structured-data/job-posting)).

### Adoption and field coverage

| Measure | Figure | Source |
|---|---|---|
| Growth 2020–2022 | About 9K to 50K+ sites, on about 4.1M URLs | [W3C list summary of WDC/Brinkmann et al.](https://lists.w3.org/Archives/Public/public-vc-edu/2023Sep/0002.html) |
| WDC subset, Oct 2024 corpus | 3,606,092 URLs on 63,320 hosts | [WDC 2024-12 subsets](https://webdatacommons.org/structureddata/2024-12/stats/schema_org_subsets.html) |
| Field coverage, 2019 sample (JSON-LD vs microdata) | datePosted 99% vs 64%; hiringOrganization 98% vs 59%; validThrough 60% vs 23%; baseSalary 47% vs 21%; identifier 41% vs 7% | [Skeptric](https://skeptric.com/schema-jobposting) |

- JSON-LD is markedly more complete and consistent than microdata ([Skeptric](https://skeptric.com/schema-jobposting)).
- Greenhouse boards emit "basic metadata" but no `validThrough`, `baseSalary`, `employmentType` or street address. Greenhouse says this doesn't affect Google eligibility (2026-03-02) ([Greenhouse support](https://support.greenhouse.io/hc/en-us/articles/115003185526-Job-post-visibility-on-Google-for-Jobs)).
- Don't rely on `validThrough` or `baseSalary` from markup, even on large ATS. Expiry has to be observed. *(synthesis)*
- 63K hosts undercounts employers, because one ATS host covers thousands of companies. Count companies, not hosts. *(synthesis)*
- The 2019 coverage figures are old. No 2024 field-level figures were found.

## Google for Jobs

- **Not a source you can read.** It indexes markup from job pages and has no consumer API ([Joveo](https://www.joveo.com/google-for-jobs-the-ultimate-guide/)). The only programmatic route is a SERP API. *(synthesis)*
- **Policies:**
  - No expired postings: set `validThrough` in the past, return 404/410, or remove the markup.
  - Markup on single-job pages only, never on list pages.
  - The markup must match the visible content.
  - Descriptions must be complete.
  - No login wall, no fees.
  - [Google](https://developers.google.com/search/docs/appearance/structured-data/job-posting)
- **Indexing API:** only for pages with JobPosting or BroadcastEvent. It needs a service account and Search Console ownership, and abuse can revoke access (updated 2026-10-16) ([Indexing API quickstart](https://developers.google.com/search/apis/indexing-api/v3/quickstart)). Google recommends it over sitemaps for job URLs ([Google](https://developers.google.com/search/docs/appearance/structured-data/job-posting)). It is for URLs you own, not for discovering other people's jobs. *(synthesis)*
- **Status 2024–2026:** no official announcement retires or reshapes the jobs feature.
  - 2024: Google added EEA-only aggregator units for DMA compliance, including "Jobs sites" ([SEJ](https://www.searchenginejournal.com/google-is-rolling-out-new-search-features-in-europe/508439/)).
  - 2026: the redesigned EEA aggregator unit lists hotels, flights, trains and products, but not jobs ([SEJ](https://www.searchenginejournal.com/google-rolls-out-redesigned-search-results-across-the-eea/588870/)).
  - The EC fined Google EUR 460M on 2026-07-23 for search self-preferencing ([NEMO tracker](https://nemo-europe.com/research/trackers/google-dma-search/)).
  - Vendor commentary on AI Mode changing job visibility is opinion ([Joveo](https://www.joveo.com/blog/google-ai-mode-google-for-jobs/)).
- **The aggregator tension** (scraped jobs vs "without authorization") is covered in [legal-and-ethics.md](legal-and-ethics.md).

## Sitemaps, RSS and distribution feeds

- **Distribution feeds are private contracts, not open sources.**
  - Indeed Job Sync XML is crawled 4 times a day or pulled from FTP every 2h ([Indeed Job Sync XML](https://docs.indeed.com/job-sync-xml/xml-feed)).
  - LinkedIn polls feeds every 6h (vendor claim) ([SCALIS](https://help.scalis.ai/linkedin-job-wrapping-via-xml-feed-free-limited-listings)).
  - Meta has its own Jobs XML spec ([Meta](https://developers.secure.facebook.com/docs/jobs-xml/specification)).
- **Their schemas are a good normalisation target anyway.** Indeed separates `referencenumber` (unique per posting instance) from `requisitionid` (which may repeat across postings), and requires the `url` to be the description page, not the application page ([Indeed](https://docs.indeed.com/job-sync-xml/xml-feed)). *(synthesis on its usefulness)*
- Greenhouse tells *customers* to include a sitemap or RSS/Atom feed with `lastmod`. That is not a promise that Greenhouse provides one itself ([Greenhouse support](https://support.greenhouse.io/hc/en-us/articles/115003185526-Job-post-visibility-on-Google-for-Jobs)).
- For open discovery, sitemaps with `lastmod` and the ATS public JSON APIs are the practical channels. *(synthesis)*

## Common Crawl and Web Data Commons

- **Web Data Commons (WDC)** has extracted schema.org data from Common Crawl every year since 2013. The 2024-12 release covers 12.27M domains ([WDC](https://webdatacommons.org/structureddata/schemaorg/)).
- **Common Crawl's URL index** comes in two forms: a CDX server and a Parquet columnar index of about 300 GB per monthly crawl, billed by bytes scanned on Athena ([Common Crawl blog](https://commoncrawl.org/blog/index-to-warc-files-and-urls-in-columnar-format)). The latest crawl on 2026-10-19 was CC-MAIN-2026-39 ([collinfo](https://index.commoncrawl.org/collinfo.json)).
- **Limits of URL heuristics** ([Skeptric](https://skeptric.com/common-crawl-job-ads)):
  - `/job/` patterns miss `/careers/`.
  - They pick up articles and listing pages.
  - Sites blocked by robots.txt are absent.
  - Each crawl is a single snapshot.
- **Data quality in the wild:** double-encoded HTML, non-ISO dates, placeholders ("UNAVAILABLE", geo 0,0), and "€" instead of "EUR" ([Skeptric](https://skeptric.com/schema-jobposting)).
- **Rule of thumb:** a yearly corpus is far too stale for job content, since most postings expire within weeks. It is useful for finding employers and ATS hosts. See [company-discovery.md](company-discovery.md). *(synthesis)*

## Search APIs as discovery

| Tool | What it gives | Notes |
|---|---|---|
| SerpApi Google Jobs | `jobs_results` with `apply_options` (every board carrying the job), `job_id`, posted-at and salary extensions; 10 per page via `next_page_token` | Google dropped the `start` offset and deprecated `ltype` ([SerpApi](https://serpapi.com/google-jobs-api)). Pricing in [big-boards-and-data-vendors.md](big-boards-and-data-vendors.md) |
| Exa | `includeDomains` up to 1,200 entries, accepting host+path prefixes and wildcard subdomains; published-date filters; max 100 results | No jobs category ([Exa](https://exa.ai/docs/reference/search)) |
| Google/Bing/Brave `site:` queries | Enumerate boards on ATS hosts | Bing Search API reportedly retired Aug 2026 ([YvetteZheng0812 README](https://github.com/YvetteZheng0812/ats-job-scraper)); Brave not researched |

- An ATS host list used as a domain filter turns a search API into a slug finder. The ATS API then gives the full, fresh board. That beats parsing markup page by page. *(synthesis)*
- `apply_options` is a ready-made cross-board duplicate signal. *(synthesis)*

## Failure modes

- **Stale postings:** `validThrough` missing or wrong, and markup left on expired pages. Google's bans imply both happen ([Google](https://developers.google.com/search/docs/appearance/structured-data/job-posting); [Skeptric](https://skeptric.com/schema-jobposting)).
- **Evergreen posts:** "General Application" or "Talent Community" posts get flagged, and Google may remove all of an organisation's posts without alert ([Greenhouse support](https://support.greenhouse.io/hc/en-us/articles/115003185526-Job-post-visibility-on-Google-for-Jobs)).
- **One role, many postings:** a repeating `requisitionid` across postings ([Indeed](https://docs.indeed.com/job-sync-xml/xml-feed)).
- No quantitative data was found on the share of duplicate or expired postings on the open web.

## Disagreements

- **Google's required set:** Google's own list differs slightly from a third-party guide, which also adds a "600 characters" description rule that Google doesn't state ([jobboardly](https://www.jobboardly.com/blog/google-jobs-api-integration-guide) vs [Google](https://developers.google.com/search/docs/appearance/structured-data/job-posting)).
- **WDC growth:** "9K to 50K+" (2020–2022) vs 63,320 hosts (2024). Consistent with growth, but counted on different corpora.
- **LinkedIn polling:** 6h, or 24h for partners, with a 500K-jobs cap. Vendor pages only.
- **Reported 2025 Indexing API restrictions favouring direct employers:** unverified, and not in Google's Oct 2026 quickstart.

## Sources

- [schema.org JobPosting](https://schema.org/JobPosting)
- [Google Search Central: job posting structured data](https://developers.google.com/search/docs/appearance/structured-data/job-posting); [Indexing API quickstart](https://developers.google.com/search/apis/indexing-api/v3/quickstart)
- [WDC schema.org data](https://webdatacommons.org/structureddata/schemaorg/); [WDC 2024-12 subsets](https://webdatacommons.org/structureddata/2024-12/stats/schema_org_subsets.html); [W3C list summary](https://lists.w3.org/Archives/Public/public-vc-edu/2023Sep/0002.html); [Brinkmann et al. WWW 2023](https://www.uni-mannheim.de/media/Einrichtungen/dws/Files_Research/Web-based_Systems/pub/Brinkmann-etal-TheWDCSchemaorgDataSetSeries-WWW2023.pdf)
- [Skeptric: JobPosting schemas in practice](https://skeptric.com/schema-jobposting); [Skeptric: Common Crawl job ads](https://skeptric.com/common-crawl-job-ads)
- [Greenhouse: Google for Jobs visibility](https://support.greenhouse.io/hc/en-us/articles/115003185526-Job-post-visibility-on-Google-for-Jobs)
- [Joveo](https://www.joveo.com/google-for-jobs-the-ultimate-guide/); [Joveo AI Mode](https://www.joveo.com/blog/google-ai-mode-google-for-jobs/); [SEJ 2024](https://www.searchenginejournal.com/google-is-rolling-out-new-search-features-in-europe/508439/); [SEJ 2026](https://www.searchenginejournal.com/google-rolls-out-redesigned-search-results-across-the-eea/588870/); [NEMO tracker](https://nemo-europe.com/research/trackers/google-dma-search/)
- [Indeed Job Sync XML](https://docs.indeed.com/job-sync-xml/xml-feed); [SCALIS](https://help.scalis.ai/linkedin-job-wrapping-via-xml-feed-free-limited-listings); [Meta Jobs XML](https://developers.secure.facebook.com/docs/jobs-xml/specification)
- [Common Crawl columnar index](https://commoncrawl.org/blog/index-to-warc-files-and-urls-in-columnar-format); [collinfo.json](https://index.commoncrawl.org/collinfo.json)
- [SerpApi Google Jobs API](https://serpapi.com/google-jobs-api); [Exa search reference](https://exa.ai/docs/reference/search); [YvetteZheng0812/ats-job-scraper](https://github.com/YvetteZheng0812/ats-job-scraper); [jobboardly](https://www.jobboardly.com/blog/google-jobs-api-integration-guide)
