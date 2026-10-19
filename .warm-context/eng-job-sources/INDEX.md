# Engineering and tech job sources and APIs

> This pack is a partial sample of the domain, not its boundary. If something isn't here, it wasn't researched; that doesn't mean it doesn't exist. When the task needs it, say so and offer a gap pass (`/warm-context eng-job-sources`).

## Scope
- **Goal:** (a) a Claude skill that runs ad-hoc engineering/tech job research on the web; (b) a website that continuously aggregates any engineering & technology opening worldwide
- **Constraints:** global; all seniorities, locations, company types; all eng/tech roles
- **Volatility:** fast-moving
- **Researched:** 2026-10-19 (updated 2026-10-19)
- **Sources used:** web

## Coverage
- **Covered:** source landscape (boards alive in 2026); ATS public job APIs; aggregator, board and government APIs and their terms; scraping big boards and commercial job-data vendors; legal and ethics (US, EU, Brazil); structured data and web-scale discovery; company/ATS-slug discovery; data quality (dedup, freshness, ghost/scam jobs, classification, normalisation); logged-out behaviour of posting links on major boards and ATS (single non-browser requests); regional boards in LATAM, Europe, India, East and SE Asia, Middle East, Africa, Canada, AU/NZ (Programathor, GeekHunter, Trampos, Jobs.ch, Instahyre, Cutshort, foundit, Wantedly, 104, Japan and Korea boards, Workopolis, Jobberman, BrighterMonday, Fuzu and others)
- **Seen but not researched:**
  - What a person in a residential browser sees on boards that blocked scripts (Indeed, Glassdoor, ZipRecruiter, SEEK, StepStone, Naukri, WTTJ www)
  - Each board's terms of service on deep-linking and automated access (none read); Trade Me Jobs API terms
  - Closed-link behaviour on Wellfound, Dice and Built In; whether Wellfound's bare `/jobs/<id>` resolves; regional host variants sharing IDs
  - Bundesagentur Jobbörse as a board; Jobindex's crawling of employer sites
  - More regional boards: Pracuj.pl, Bulldogjob, DOU.ua, Profession.hu; Apna, Shine; Levtech, Forkwell, TokyoDev, Japan Dev; Programmers, Jumpit; VietnamWorks, TopCV; Wuzzuf, Akhtaboot; Talent.com, Eluta
  - Government feeds: Workforce Australia and APS Jobs open data; Fair Consideration Framework rules behind MyCareersFuture
  - BOSS Zhipin deep pages and anti-bot behaviour from abroad
  - Reddit, Discord/Slack communities, job newsletters; remote-jobs GitHub lists
  - Smaller ATS: Pinpoint, Gem, Dover, Polymer, Jobvite's feed, SuccessFactors/Phenom first-hand details; full Workable/Teamtailor/Greenhouse Harvest APIs
  - Vendors: JobsPikr, Mantiks, Crustdata, NinjaPear, Unipile, JobFront, DataForSEO Google Jobs, jobo.world; TheirStack/Kadence ATS market data
  - Indeed Hiring Lab and Appcast reports; Appcast/programmatic feed formats
  - Company seeds: Crunchbase, Dealroom, PitchBook, OpenCorporates, Wikidata, BuiltWith/Wappalyzer, crt.sh; Simplify and levels.fyi discovery methods
  - Brave Search API and Bing APIs
  - Legal: UK database right and ICO position, trespass to chattels, *Feist* and fair use for snippets, CCPA "publicly available", Clearview fines, later *X v. Bright Data* history, *Kneschke v. LAION* BGH outcome
  - Fake-recruiter and North Korean IT-worker scams; FBI IC3 2025 figure
  - Colorado/NYC/California pay rules, currency conversion, seniority inference, multilingual postings
  - W3C Talent Signal / Job Data Exchange, Zyte job schema
- **Out of scope:** the website's own tech stack and hosting; career advice

## Files
- [overview.md](overview.md): the core mental model; read first
- [source-landscape.md](source-landscape.md): what kinds of job sources exist, which are alive in 2026, and do posting links work logged out?
- [regional-boards.md](regional-boards.md): which regional eng/tech boards matter outside the big global ones, and how open are they?
- [ats-job-apis.md](ats-job-apis.md): which ATS expose public job feeds, and how?
- [aggregator-and-board-apis.md](aggregator-and-board-apis.md): which official or free board, aggregator and government APIs exist, and on what terms?
- [big-boards-and-data-vendors.md](big-boards-and-data-vendors.md): what does scraping LinkedIn/Indeed/Glassdoor involve, and what does commercial job data cost?
- [legal-and-ethics.md](legal-and-ethics.md): what may be collected, stored and redisplayed (US, EU, Brazil)? Background, not legal advice
- [structured-data-and-discovery.md](structured-data-and-discovery.md): how do schema.org JobPosting, Google for Jobs, Common Crawl and search APIs help find postings?
- [company-discovery.md](company-discovery.md): how do aggregators find companies and their ATS slugs?
- [data-quality.md](data-quality.md): how do aggregated postings go wrong (dedup, freshness, ghost/scam jobs, classification, normalisation)?
