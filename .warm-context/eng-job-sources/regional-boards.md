# Which regional eng/tech boards matter outside the big global ones, and how open are they?

Covers boards by region, the ownership groups that copy one ad across many sites, robots.txt limits on endpoints that answer anyway, and changes in 2024–2026. The global boards are in [source-landscape.md](source-landscape.md). The free APIs already covered (Reed, Arbeitnow, Canada Job Bank) are in [aggregator-and-board-apis.md](aggregator-and-board-apis.md).

## How to read the tables

- **Status:** "200" or "403" is the HTTP result of one plain GET of a homepage, listing or posting, observed 2026-10-19 from non-browser clients (curl, and a hosted fetch tool). A 403 means a non-browser client is blocked, usually by a bot-protection service. It does not prove a login wall or a region block; a person in a browser was not tested. See [source-landscape.md](source-landscape.md#do-posting-links-work-logged-out).
- **Public link:** whether individual postings have a stable detail URL a logged-out visitor can open. "Indexed" means detail URLs show up in search-engine results even when our fetch was blocked.
- **Feed/API:** public JSON, RSS or an official API for reading jobs. "Answers" means it returned data without a key on 2026-10-19.
- **Terms:** no board's terms of service were read in this pass. The column records what robots.txt or the API docs say, or "not read".
- **(vendor)** marks a figure from the company or a seller of scrapers or recruiting tools.

## Three kinds of regional board

1. **ATS-backed portals.** The board is the front end of an applicant tracking system (ATS, the software employers use to post jobs and manage applicants). Postings are first-party and the canonical URL is on the employer's ATS subdomain. Examples: Gupy, Sólides, JOIN.
2. **Classic paid-ad boards.** Employers or agencies buy ad slots. Examples: Computrabajo, Bumeran, OCC, Reed, Totaljobs, jobs.ch, Finn, Jobs.cz.
3. **Curated tech marketplaces.** Small, tech-only, often reverse recruiting (companies approach candidates). They publish few public postings because the product is the candidate pool. Examples: GeekHunter, Revelo, Coodesh, Torre, Instahyre, Findy, OfferZen.

For an aggregator, kind 1 is best reached through the ATS, kind 2 is mostly copies plus agency ads, and kind 3 adds little public supply. *(synthesis)*

## Brazil and LATAM

| Board | Status | Tech focus | Public link, no login | Feed/API | Terms |
|---|---|---|---|---|---|
| Gupy (BR) | 200 | All sectors; the largest BR hiring ATS, 4,000+ companies (vendor, undated) ([Gupy](https://www.gupy.io/blog/manifesto-da-pessoa-candidata-da-gupy)) | Yes: `<company>.gupy.io/jobs/<id>` returned 200 (observed 2026-10-19) | Official API needs a company-bound token ([Gupy forum](https://developers.gupy.io/discuss/64cb9a32aebeb70b037dcf40)); old portal JSON returned 404 (observed 2026-10-19) | Not read. See [Gupy as an ATS](#gupy-is-an-ats-first-and-a-board-second) |
| Programathor (BR) | Listing 200; detail pages 500 (observed 2026-10-19) | Dev-only since 2017 ([Betterteam](https://www.betterteam.com/br/programathor)) | Pattern `programathor.com.br/jobs/<id>-<slug>`; not confirmed to load | None found | Not read |
| GeekHunter (BR) | 200; `geekhunter.com.br` redirects to `geekhunter.com/pt/vagas`, showing 763 jobs (observed 2026-10-19) | Tech-only reverse recruiting; ~400k professionals, 13k+ companies (vendor, undated) ([GeekHunter](https://www.geekhunter.com.br/downloads/Pesquisa_Salarial.pdf)) | Yes: `geekhunter.com/pt/<company>/jobs/<slug>` returned 200 | None | robots.txt disallows `/api/` and `/vagas-` paths; Content-Signals `search=yes, ai-input=yes, ai-train=no` ([robots.txt](https://www.geekhunter.com/robots.txt), observed 2026-10-19) |
| Trampos (BR) | 200 | Marketing and comms plus IT ([Catraca Livre](https://catracalivre.com.br/rede/trampos/)) | Yes: `trampos.co/oportunidades/<id>` | **Answers:** `trampos.co/api/v2/opportunities?page=N`, 12 a page, 179 open (observed 2026-10-19) | No published API terms found |
| Sólides Vagas (BR) | 200, "+65 mil Oportunidades" in the title (observed 2026-10-19) | All sectors; portal for Sólides ATS clients ([Diário do Comércio](https://diariodocomercio.com.br/economia/solides-lanca-portal-de-vagas-de-trabalho/)) | JS app; no detail links in the HTML (observed 2026-10-19) | None found | Not read |
| BNE (BR) | 200; claims 1,681,017 jobs (vendor) ([BNE](https://www.bne.com.br/vagas-de-emprego)) | All sectors, with a `/jobs/bne-tech` section | Yes: `bne.com.br/vaga-de-emprego-na-area-…/<title>/<id>` | None found | Not read |
| Revelo, Coodesh (BR) | 200, but JS shells with no posting links (observed 2026-10-19) | Revelo now places LATAM engineers with US companies ([Startups.com.br](https://startups.com.br/negocios/ma/no-embalo-da-ia-revelo-empilha-mas-e-quer-consolidar-na-america-latina/)); Coodesh sells dev assessments ([B2B Stack](https://www.b2bstack.com.br/product/coodesh)) | No | None (Coodesh `/api/jobs` 404, observed 2026-10-19) | Not read |
| Get on Board (LATAM, from CL) | 200 | Tech-first; ~314 programming jobs (observed 2026-10-19) | Yes: `getonbrd.com/jobs/<slug>` | **Public API v0, no key**, for "information that is already visible publicly" ([Get on Board](https://www.getonbrd.com/help/que-puedo-hacer-con-la-api-de-get-on-board?lang=en)); mirrored at jobs.platzi.com ([Platzi](https://jobs.platzi.com/user-manual/get-on-board-s-api)) | No stated rate limits or attribution rules |
| Computrabajo (18 Spanish-speaking countries, no BR) | 200 | General, very large | Yes: `mx.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-<slug>-<hexid>` (observed 2026-10-19) | None | Not read. Redarbor group |
| OCC Mundial (MX) | 200 | General; "largest in Mexico" (vendor) | Listing loads; detail links are JS-rendered (observed 2026-10-19) | None | Not read. Redarbor group |
| Bumeran (AR, CL, EC, PE, PA, MX, CO) | 200 but an empty shell to a script (observed 2026-10-19) | General ([Gestión](https://gestion.pe/economia/empresas/bumeran-busca-ampliar-cartera-de-clientes-en-regiones-apalancado-en-nuevas-inversiones-noticia/)) | JS-rendered | None | Not read. Jobint group |
| Torre (LATAM, remote) | Redirects to `app.torre.ai/search-job` (observed 2026-10-19) | AI matching, remote-heavy | App only | Official API is "beta, limited access", by request ([Torre](https://torre.ai/es/apiforprofessionals); [request form](https://torre.ai/request-api)) | Not read |

Catho, InfoJobs BR and Vagas.com.br are in [source-landscape.md](source-landscape.md).

## Europe

| Board | Status | Tech focus | Public link, no login | Feed/API | Terms |
|---|---|---|---|---|---|
| NoFluffJobs (PL, CEE) | 200 | IT-only; salary mandatory | Yes: `nofluffjobs.com/pl/job/<slug>` | `/api/posting` **answers** without a key, a dump over 100 MB (observed 2026-10-19) | robots.txt `Disallow: /api/` (observed 2026-10-19) |
| Just Join IT (PL) | 200 | IT-only; 110,996 postings in 2025, peak 175,610 in 2022 ([Brandsit](https://brandsit.pl/?p=1971322)) | Yes: `justjoin.it/job-offer/<slug>` | API host returned 503 (observed 2026-10-19) | robots.txt `Disallow: /api/` |
| Djinni (UA) | 200 | IT-only, anonymous profiles; ~27k vacancies in Q2 2025, >8k active ([Mezha](https://mezha.ua/news/it-vakansiji-v-ukrajini-zrostaye-kilkist-propoziciji-dlya-data-specialistiv-rekruteriv-ta-devopsiv-303221/)) | Yes: `djinni.co/jobs/<id>-<slug>/` | **RSS** `djinni.co/jobs/rss/`, 100 items, keyword filter works (observed 2026-10-19) | Not read |
| Landing.jobs (PT) | 200 | Tech-only | Yes: `landing.jobs/at/<company>/<slug>` | **Answers:** `landing.jobs/api/v1/jobs`, 50 a page, with salary fields (observed 2026-10-19) | Not read |
| Berlin Startup Jobs (DE) | 200; 138 engineering jobs (observed 2026-10-19) | Startup tech | Yes (WordPress posts) | **RSS per category** (`/engineering/feed/` 200); site-wide `/feed/` 403 (observed 2026-10-19) | Not read |
| JOIN (DE/EU) | 200 | All sectors; a free ATS with multiposting to 10+ boards including Indeed, LinkedIn, XING, Glassdoor (vendor) ([JOIN](https://join.com/en/features/multiposting)) | Company career pages on join.com | No board API; feeds Arbeitnow ([Arbeitnow](https://www.arbeitnow.com/blog/job-board-api)) | Not read |
| Welcome to the Jungle UK/FR (ex-Otta) | `otta.com` 301 to `uk.welcometothejungle.com` (observed 2026-10-19) | Startup and tech, curated | Yes on the `app.` host; the www host returned 403 ([source-landscape.md](source-landscape.md#do-posting-links-work-logged-out)) | None public | Not read |
| jobs.ch / jobup.ch (CH) | 200; 503 dev jobs on a jobs.ch query (observed 2026-10-19) | General; No.1 in Switzerland (vendor) ([JobCloud](https://jobcloud.ch/c/en/about)) | Yes: `jobs.ch/en/vacancies/detail/<uuid>/` | None | robots.txt disallows `/api/` and deep detail paths ([robots.txt](https://www.jobs.ch/robots.txt), observed 2026-10-19) |
| Totaljobs / CWJobs (UK) | 403 to a script (observed 2026-10-19) | General / IT-specialist ([idibu](https://idibu.com/network/totaljobs)) | Not verified | None public | Not read. StepStone group |
| Indeed DE | 403 to a script (observed 2026-10-19) | General | Not verified | Publisher API "no longer maintained" ([Arbeitnow](https://www.arbeitnow.com/blog/job-board-api)) | Not read |
| Jobs.cz (CZ) | 200 | General | Many ads redirect to employer microsites `<company>.jobs.cz` (observed 2026-10-19) | None | robots.txt disallows `/api/` and `/iapi/` |
| Jobindex (DK) | 200; ~35k jobs live ([Jobindex](https://www.jobindex.dk/virksomhed/57305/robot-nordic-aps?lang=en)) | General | Yes | **RSS** `jobindex.dk/jobsoegning.rss?q=…` (observed 2026-10-19) | robots.txt disallows `/api/` |
| Finn.no jobb (NO) | 200 | General | Yes: `finn.no/job/ad/<id>` | None | **robots.txt: crawling prohibited without written permission** ([robots.txt](https://www.finn.no/robots.txt), observed 2026-10-19) |

Reed and Arbeitnow have free APIs and are in [aggregator-and-board-apis.md](aggregator-and-board-apis.md). Reed's API terms are not published; one third-party author reads Reed's site terms as forbidding a competing board ([JobsPipe](https://jobspipe.dev/blog/reed-api)).

## India

| Board | Status | Tech focus | Public link, no login | Feed/API | Terms |
|---|---|---|---|---|---|
| Naukri | Connection dropped at the edge (observed 2026-10-19) | General, the largest; covered in [source-landscape.md](source-landscape.md) | Not verified | None; a scraper vendor says plain requests hit an Akamai bot check ([Apify](https://apify.com/leadsbrary/naukri-jobs-scraper)) | Not read |
| Cutshort | 200 | Tech-first, also product, design, sales (vendor) ([Cutshort](https://cutshort.io/best-platforms-to-hire-software-engineers-in-india)) | **Yes:** `cutshort.io/job/<Title>-<City>-<Company>-<id>`, salary and skills visible (observed 2026-10-19) | None official | Not read |
| Hirist (hirist.tech) | 200 | IT-only; owned by Info Edge (Naukri's parent) since 2019 ([People Matters](https://www.peoplematters.in/news/entrepreneurship-start-ups/info-edge-acquires-iimjobs-for-rs-8082-cr-21833)) | Category, skill and city pages are public; detail pattern not confirmed (observed 2026-10-19) | None found | Not read |
| Instahyre | 403 (observed 2026-10-19) | Curated tech; matched "opportunities" inside an account ([Instahyre help](https://help.instahyre.com/en/article/explore-matching-opportunities-1s98q42/)) | Weak: the model is account-based | None found | Not read |
| foundit (ex-Monster India/APAC/ME) | 403 (observed 2026-10-19); still publishing hiring reports in 2026 ([HRKatha](https://www.hrkatha.com/tag/foundit/)) | General; India, SE Asia, Gulf; 70M job seekers claimed in 2022 (vendor) ([Marketech APAC](https://marketech-apac.com/job-search-portal-monster-com-rebrands-as-foundit/)) | Not verified | None found | Not read |
| Internshala | 200 | Internships and fresher jobs only; 90% bought by upGrad in Feb 2026 ([Staffing Industry](https://www.staffingindustry.com/news/global-daily-news/indias-upgrad-acquires-90-stake-in-internshala)) | Detail pattern not checked | None found | Not read |

Wellfound shows about 5k India roles with INR salary and equity ([Wellfound](https://wellfound.com/location/india?page=4)).

## Japan, Korea, Taiwan and China

These boards are mostly native-language only. Cake (Taiwan) and Yourator are the most English-friendly ([resumegeni](https://resumegeni.com/blog/how-to-write-resume-taiwan)).

| Board | Status | Tech focus | Public link, no login | Feed/API | Terms |
|---|---|---|---|---|---|
| Green (JP) | 200 | IT ventures; run by Atrae ([atsoho](https://atsoho.com/blog/it-tenshoku-hikaku-site)) | **Yes:** `green-japan.com/company/<cid>/job/<jid>`, salary on cards (observed 2026-10-19) | None found | Not read |
| Wantedly (JP) | 200 | Startups, casual-interview "projects" | **Yes:** `wantedly.com/projects/<id>`, no login prompt (observed 2026-10-19) | None found | Not read |
| Findy (JP) | 200 | Skilled engineers, scored from GitHub; 200k users claimed (vendor) ([BizReach ad](https://www.bizreach.jp/job/view/9019020/)) | Partial: company job pages at `/companies/<id>/jobs` ([Findy](https://findy-code.io/)) | None found | Not read |
| doda (JP, Persol) | Dropped from one network, loaded from another (observed 2026-10-19) | General; claims 50,000+ IT engineer jobs (vendor) ([doda](https://doda.jp/engineer/)) | Search URLs public; detail pattern not seen | None found | Not read |
| BizReach (JP) | 200 | High-salary and executive scouting | Partial: `bizreach.jp/job/view/<id>/` is public but "company names are shown to members only" (observed 2026-10-19) | None found | Not read |
| Wanted (KR) | 200 | Tech-focused; shows salary bands ([seoulstart](https://seoulstart.com/guides/best-job-sites-korea)) | **Yes:** `wanted.co.kr/wd/<id>` | Internal front-end JSON `wanted.co.kr/api/v4/jobs` **answers** without a key; undocumented (observed 2026-10-19) | No published terms found |
| Saramin (KR) | 200; 2,453 results for 백엔드 (backend) (observed 2026-10-19) | General, one of Korea's two largest ([seoulstart](https://seoulstart.com/guides/korean-job-platforms)) | JS-rendered; detail pattern not confirmed | `oapi.saramin.co.kr` redirected to an error page (observed 2026-10-19) | Not read |
| JobKorea (KR) | 200 | General, the other of the two largest; parent Worxphere ([seoulstart](https://seoulstart.com/guides/korean-job-platforms)) | Not checked | None found | Not read |
| 104 Job Bank (TW) | 403 (observed 2026-10-19) | The dominant general board; 1111 is second ([resumegeni](https://resumegeni.com/blog/how-to-write-resume-taiwan)) | Indexed: `104.com.tw/job/<id>` ([example](https://www.104.com.tw/job/similar/8752o?page=3)) | None found | Not read |
| Cake (TW, ex-CakeResume) | curl 200, hosted fetch 403 (observed 2026-10-19) | Tech and design; 7M users claimed (vendor, 2024) ([INSIDE](https://www.inside.com.tw/article/35488-cake-rebranding)) | Yes: `cake.me/jobs/…` | None found | robots.txt allows all and lists a sitemap (observed 2026-10-19) |
| Zhaopin (CN) | 200 | Large general board | **Yes:** `zhaopin.com/jobdetail/<id>.htm`; applying pushes to the app (observed 2026-10-19) | None found | Not read |
| Liepin (CN) | 200 | Mid-to-senior and headhunters | SEO pages public (`/zhaopin/`, `/career/<id>/`); detail pattern not seen | None found | Not read |
| 51job (CN) | 200 | Large general board | Search is client-rendered, only a title came back (observed 2026-10-19) | None found | Not read |
| BOSS Zhipin (CN) | Homepage 200 (observed 2026-10-19) | Chat-first app; covered in [source-landscape.md](source-landscape.md) | Deep pages not tested | None found | Not read |

Signing up on Chinese boards needs a mainland mobile number, and one author reports connections refused or challenged from abroad ([Second Talent](https://www.secondtalent.com/resources/job-boards-to-hire-employees-in-china/)). Lagou, once the tech specialist, is in bankruptcy reorganisation (see [status changes](#status-changes-20242026)).

## Southeast Asia

| Board | Status | Tech focus | Public link, no login | Feed/API | Terms |
|---|---|---|---|---|---|
| MyCareersFuture (SG, government) | 200 | All jobs. Employers under Singapore's Fair Consideration Framework must advertise here (background, not re-verified) | **Yes:** `mycareersfuture.gov.sg/job/<category>/<slug>-<uuid>` | **Open JSON** `api.mycareersfuture.gov.sg/v2/jobs?search=…`, no key, with salary range, skills, occupation code, posting and expiry dates; 851 results for "software engineer" (observed 2026-10-19). Undocumented | No terms page found |
| Jobstreet / Jobsdb (SG, MY, PH, ID, HK, TH) | 403 on SEEK hosts (observed 2026-10-19) | General; one SEEK platform since 2024 ([Jobstreet](https://my.jobstreet.com/about/news/article/seek-jobstreet-jobsdb-unify)) | Not verified | Approval-only SEEK API, for posting not reading ([SEEK developer](https://developer.seek.com/)) | Not read |
| ITviec (VN) | 403 (observed 2026-10-19) | IT-only; 10k+ IT companies claimed (vendor) ([ITviec](https://itviec.com/employer)) | Indexed: `itviec.com/it-jobs/<slug>-<id>` ([example](https://itviec.com/it-jobs/principal-backend-engineer-itviec-recruitment-consulting-5728)) | None found | Not read |
| TopDev (VN) | 200 | IT recruiting; 350k developer profiles claimed (vendor) ([webcatalog](https://webcatalog.io/pl/apps/topdev)) | Not checked | None found | Not read |
| Glints (ID, SG, MY, VN, PH, TW) | 403 (observed 2026-10-19) | General, strongest in Indonesia; headcount down 27% from 2023 to 2026 (estimate) ([Revelio](https://www.reveliolabs.com/companies/glints/employees)) | Not verified | None found | Not read |
| NodeFlair (SG) | 403 (observed 2026-10-19) | Tech jobs plus 130k+ salary data points ([Vulcan Post](https://vulcanpost.com/911031/nodeflair-2026-singapore-tech-salaries/)) | Not verified | None found | Not read |
| Kalibrr (PH, ID) | Indexed | General with tech | Yes: `kalibrr.com/c/<company>/jobs/<id>/<slug>`; many stale postings indexed ([example](https://www.kalibrr.id/c/kalibrr-ph/jobs/215/associate-software-engineer)) | None found | Not read |

## Middle East

| Board | Status | Tech focus | Public link, no login | Feed/API | Terms |
|---|---|---|---|---|---|
| Bayt | 403 (observed 2026-10-19) | Regional incumbent, all levels; 52M+ CVs claimed (vendor) ([ksaexpats](https://ksaexpats.com/best-job-sites-in-saudi-arabia/)) | Not verified; no detail URLs found in search | None found | Not read |
| GulfTalent | 403 (observed 2026-10-19) | Mid-to-senior engineering and management; "551 Software Engineer jobs in Dubai" on an indexed page ([GulfTalent](https://www.gulftalent.com/uae/jobs/dubai/title/software-engineer)) | Results pages indexed | None found | Not read |
| Naukrigulf | 403 (observed 2026-10-19) | Info Edge; used to source Indian and Pakistani tech candidates (vendor) ([100hires](https://100hires.com/uae-job-sites.html)) | Not verified | None found | Not read |

## Africa

| Board | Status | Tech focus | Public link, no login | Feed/API | Terms |
|---|---|---|---|---|---|
| Jobberman (NG, GH) | 200 | General, with a "Software & Data" category; Ringier One Africa Media ([TechCabal](https://techcabal.com/fr/2020/10/27/jobberman-acquisition-ng-careers-roam-africa/)) | **Yes:** `jobberman.com/listings/<slug>-<6char>`, NGN salary often shown ([example](https://www.jobberman.com/listings/software-developer-8mpm6x)) | None found | Not read |
| PNet (ZA) | 403 (observed 2026-10-19) | Largest ZA general board; StepStone group, rebranded Jun 2025 ([Daily Maverick](https://www.dailymaverick.co.za/article/2025-06-24-pnet-rebrands-to-empower-south-african-jobseekers-and-recruiters-with-global-innovation.md)); "1,796 Software Developer jobs in Gauteng" ([PNet](https://pnet.co.za/jobs/software-developer/in-gauteng)) | Results pages indexed | None found | Not read |
| Careers24 (ZA) | 403 (observed 2026-10-19) | General; Media24 / Naspers | Company pages indexed | None found | Not read |
| BrighterMonday (KE, UG, TZ) | 200 | General East Africa since 2006 ([achisystems](https://achisystems.co.ke/directory/top-20-websites-for-jobs-in-kenya-2026/)) | Not checked | None found | Not read |
| Fuzu (KE, NG, UG) | 403 (observed 2026-10-19); reportedly pivoting to AI data-operations teams ([africaglobalfunds](https://africaglobalfunds.com/news/investors/finnishkenyan-recruitment-platform-raises-175m-from-finnfund-and-others/)) | General | Indexed `fuzu.com/job/<region>` | None found | Not read |
| OfferZen (ZA) | 200; "South Africa's largest tech talent marketplace", 2,000+ companies (vendor, observed 2026-10-19) | Tech; reverse marketplace ([WeeTracker](https://weetracker.com/2024/01/30/south-africa-hrtech-offerzen-4-3m-fundraise/)) | No: profiles are private | None | Not read |

## Canada

| Board | Status | Tech focus | Public link, no login | Feed/API | Terms |
|---|---|---|---|---|---|
| Indeed CA | #1 Canadian HR site, 23.27M visits a month in Apr 2025 ([Semrush](https://nl.semrush.com/website/top/canada/jobs)) | General | Blocked to scripts, like indeed.com ([source-landscape.md](source-landscape.md#do-posting-links-work-logged-out)) | Deprecated | Not read |
| Workopolis | 403 (observed 2026-10-19) | Owned by Recruit since 2018 ([ERE](https://www.ere.net/articles/details-of-indeeds-acquisition-of-workopolis)); now a white-label portal for Indeed postings ([Manatal](https://www.manatal.com/fr/blog/niche-job-boards-canada)) | Redundant with Indeed | None | Not read |
| Jobillico (QC) | 403 (observed 2026-10-19) | General, FR/EN; #2 Canadian recruitment site by visits after Talent.com, Apr 2026 ([Semrush](https://www.semrush.com/trending-websites/ca/recruitment-and-staffing)) | Postings syndicate into Job Bank ([example](https://www.qc.jobbank.gc.ca/jobsearch/jobposting/49298197)) | Via Job Bank open data ([aggregator-and-board-apis.md](aggregator-and-board-apis.md)) | Not read |

## Australia and New Zealand

| Board | Status | Tech focus | Public link, no login | Feed/API | Terms |
|---|---|---|---|---|---|
| SEEK (AU, NZ) | 403 (observed 2026-10-19); market leader with "stable" placement share in FY2026 ([Staffing Industry](https://www.staffingindustry.com/news/global-daily-news/seek-reports-10-rise-in-full-year-net-revenue-while-profit-tumbles)) | General | Indexed `seek.com.au/job/<id>` | **Approval-only** API for posting ads, applications and ad performance, not reading ([SEEK developer](https://developer.seek.com/)). SEEK also cut off Employment Hero's access ([Employment Hero](https://employmenthero.com/nz/blog/seek-is-ending-employment-hero-api-access)) | Not read |
| Trade Me Jobs (NZ) | 406 to a script (observed 2026-10-19); one of four sources in the government's Jobs Online index ([MBIE](https://www.mbie.govt.nz/dmsdocument/32302-jobs-online-quarterly-report-june-2026)) | General | Not verified | **Official documented search API** `api.trademe.co.nz/v1/Search/Jobs.json`: 25 rows unauthenticated, 500 authenticated, rate-limited ([Trade Me](https://developer.trademe.co.nz/api-reference/search-methods/jobs-search)) | API terms not read |
| Jora (AU) | All hosts 403 (observed 2026-10-19); possibly Australia-only since 2026-09-09 (see disagreements) | SEEK-owned aggregator, so its jobs duplicate other boards | Not verified | None public | Not read |

## Ownership groups that cause cross-posting

One ad often appears on every site in a group, so dedup should know the group. *(synthesis)*

| Group | Sites | Source |
|---|---|---|
| Redarbor | Computrabajo, InfoJobs BR (2022), Catho and OCC (bought from SEEK, closed 2024-06-20, US$85M) | [Cuatrecasas](https://www.cuatrecasas.com/en/global/article/redarbor-consolidates-position-in-latam-by-acquiring-majority-stake-in-infojobs-brasil-1); [Staffing Industry](https://www.staffingindustry.com/news/global-daily-news/seek-completes-sale-latin-american-job-board-businesses-0) |
| Jobint (ex-Navent) | Bumeran, ZonaJobs, Konzerta, Laborum, Multitrabajos | [Gestión](https://gestion.pe/economia/empresas/bumeran-busca-ampliar-cartera-de-clientes-en-regiones-apalancado-en-nuevas-inversiones-noticia/); [TechCrunch](https://techcrunch.com/?p=696550) |
| StepStone | stepstone.de, Totaljobs and CWJobs (bought 2012 for £110M), PNet (ZA) | [Recruiter](https://recruiter.co.uk/news/2012/04/stepstone-buys-totaljobs-group); [Daily Maverick](https://www.dailymaverick.co.za/article/2025-06-24-pnet-rebrands-to-empower-south-african-jobseekers-and-recruiters-with-global-innovation.md) |
| JobCloud (TX Group and Ringier, 50/50) | jobs.ch, jobup.ch; 2025 revenue CHF 113.3M (−7.7%) | [TX Group](https://report.tx.group/2025/ar/en/tx-markets); [JobCloud](https://jobcloud.ch/c/en/about) |
| Alma Career (ex-LMC) | Jobs.cz, Prace.cz | [GlobeNewswire](https://www.globenewswire.com/news-release/2011/12/21/242398/0/en/Alma-Media-acquires-the-leading-online-recruitment-company-in-the-Czech-Republic.html); [LMC](https://www.lmc.eu/en/our-story) |
| SEEK | SEEK AU/NZ, Jobstreet, Jobsdb, Jora | [Jobstreet](https://my.jobstreet.com/about/news/article/seek-jobstreet-jobsdb-unify) |
| Info Edge | Naukri, Naukrigulf, Hirist, iimjobs | [People Matters](https://www.peoplematters.in/news/entrepreneurship-start-ups/info-edge-acquires-iimjobs-for-rs-8082-cr-21833) |
| Recruit | Indeed, Glassdoor, SimplyHired, Workopolis | [ERE](https://www.ere.net/articles/details-of-indeeds-acquisition-of-workopolis); [source-landscape.md](source-landscape.md) |

Multiposting ATS add a second layer: JOIN pushes one ad to 10+ free boards ([JOIN](https://join.com/en/features/multiposting)), and Cake reposts 104 jobs ([resumegeni](https://resumegeni.com/blog/how-to-write-resume-taiwan)).

## Open endpoints that robots.txt disallows

Several boards answer JSON without a key while their robots.txt (the file that tells crawlers which paths to avoid) disallows the same path. All observed 2026-10-19:

| Board | What answers | What robots.txt says |
|---|---|---|
| NoFluffJobs | `/api/posting`, a full dump over 100 MB | `Disallow: /api/` |
| Just Join IT | API host (503 on the day) | `Disallow: /api/` |
| jobs.ch | Detail pages | Disallows `/api/` and deep detail paths |
| Jobs.cz | Pages and microsites | Disallows `/api/`, `/iapi/` |
| Jobindex | RSS search feed | Disallows `/api/` |
| Finn.no | Pages | Crawling prohibited without written permission |
| GeekHunter | Posting pages | Disallows `/api/` and `/vagas-` paths; `ai-train=no` |

robots.txt is "not a form of access authorization" ([RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html)), but a disallow reads as "not for third-party reuse". It matters more for a continuous aggregator than for a skill that opens one page a user asked about. Undocumented JSON (Wanted, MyCareersFuture, Trampos) has no published terms either way. *(synthesis; legal background in [legal-and-ethics.md](legal-and-ethics.md))*

## Gupy is an ATS first and a board second

- Each client company has a career site at `<company>.gupy.io`. A posting at `stefanini.gupy.io/jobs/12737067` returned 200 (observed 2026-10-19).
- The central portal `portal.gupy.io` server-renders 100 results whose links are `<company>.gupy.io/job/<base64 of {"jobId":N,"source":"gupy_portal"}>` (observed 2026-10-19). The stable key is the numeric job ID plus the company subdomain. *(synthesis)*
- The official API at developers.gupy.io is for client companies managing their own jobs and candidates ([Gupy forum](https://developers.gupy.io/discuss/64cb9a32aebeb70b037dcf40); [Digibee](https://docs.digibee.com/documentation/connectors-and-triggers/connectors/industry-solutions/gupy)). A scraper vendor says a portal API exists but gives no path ([Apify](https://apify.com/dadosbr/gupy-vagas.md)).
- Vagas and Catho republish Gupy jobs ([Vagas](https://www.vagas.com.br/vagas-de-gupy)). For Brazil, treating Gupy as an ATS source, like Greenhouse, covers more than any one board. *(synthesis)*

## Status changes 2024–2026

| Date | Change | Source |
|---|---|---|
| Jan 2024 | Welcome to the Jungle bought Otta; `otta.com` now redirects | [StartupRise](https://startuprise.co.uk/welcome-to-the-jungle-acquired-otta/) |
| Feb 2024 | SEEK, Jobstreet, Jobsdb unified on one platform | [Jobstreet](https://my.jobstreet.com/about/news/article/seek-jobstreet-jobsdb-unify) |
| 2024-06-20 | SEEK's sale of Catho and OCC to Redarbor closed | [Staffing Industry](https://www.staffingindustry.com/news/global-daily-news/seek-completes-sale-latin-american-job-board-businesses-0) |
| 2024-07-01 | CakeResume renamed Cake | [INSIDE](https://www.inside.com.tw/article/35488-cake-rebranding) |
| 2024–2025 | Schibsted Marketplaces renamed Vend (May 2025); jobs focused on Norway, Blocket Jobs and JobbSafari closed; jobs revenue −10% in Q1 2025 | [Euronext](https://live.euronext.com/en/products/equities/company-news/2024-10-23-schibsted-asa-schaschb-schibsted-marketplaces-advances); [Vend](https://vend.com/news/interim-report-q1-2025-for-schibsted-marketplaces) |
| May 2025 | Revelo had made five acquisitions in two years and pivoted to US placements | [Startups.com.br](https://startups.com.br/negocios/ma/no-embalo-da-ia-revelo-empilha-mas-e-quer-consolidar-na-america-latina/) |
| Jun 2025 | PNet rebranded under StepStone | [Daily Maverick](https://www.dailymaverick.co.za/article/2025-06-24-pnet-rebrands-to-empower-south-african-jobseekers-and-recruiters-with-global-innovation.md) |
| Feb 2026 | upGrad bought 90% of Internshala | [Entrepreneur India](https://india.entrepreneur.com/news-and-trends/upgrad-acquires-internship-platform-internshala-in/503027) |
| 2026 | Arbeitnow launched a UK version | [Arbeitnow](https://www.arbeitnow.com/blog/job-board-api) |
| Apr–May 2026 | Lagou entered bankruptcy reorganisation, case (2026)京01破209号; app pulled from the iOS App Store | [ITHome](https://www.ithome.com/0/957/960.htm); [36Kr](https://www.36kr.com/p/3821852724568069) |
| 2026-06-08 | JobKorea's foreigner site KLiK closed | [seoulstart](https://seoulstart.com/guides/korean-job-platforms) |
| Jul 2026 | Fuzu reported moving away from a marketplace | [africaglobalfunds](https://africaglobalfunds.com/news/investors/finnishkenyan-recruitment-platform-raises-175m-from-finnfund-and-others/) |
| 2026-09-09 | Jora reportedly closed outside Australia (one vendor source) | [Actowiz](https://www.actowizsolutions.com/jora-data-scraping.php) |

Dead or pivoting regional sources (Lagou, Revelo, Fuzu, OfferZen-style marketplaces) are the ones to drop from a crawl list first; the survivors with public detail pages are mostly classic ad boards and ATS portals. *(synthesis)*

## Disagreements

- **Gupy's size:** 4,000+ companies and 2M hires ([blog](https://www.gupy.io/blog/manifesto-da-pessoa-candidata-da-gupy)) vs 4M+ hires and 50M candidates ([sales page](https://www.gupy.io/aumentar-atratividade-novos-talentos)), both vendor and undated. 2022 press says 1,500 customers ([Startups.com.br](https://startups.com.br/negocios/brazilian-hrtech-gupy-attracts-softbank-and-riverwood-in-93m-round/)).
- **Revelo's talent pool:** 300k, 400k or 1.5M depending on the source ([Convergência Digital](https://convergenciadigital.com.br/carreira/revelo-abre-600-vagas-e-usa-ia-para-seleo-dos-candidatos)).
- **JOIN pricing:** free organic multiposting ([JOIN](https://join.com/en/features/multiposting)) vs "no free plan, from €17/job/month" ([ItechGuides](https://www.itechguides.com/products/join/)).
- **Torre:** a community CLI says public endpoints need no credentials ([torre-cli](https://pkg.go.dev/github.com/jjuanrivvera/torre-cli@v0.1.3)); Torre calls its API request-only beta, and a direct request was rejected (observed 2026-10-19).
- **foundit:** "filed for bankruptcy" in June 2025 ([CB Insights](https://www.cbinsights.com/company/monster-worldwide)) vs hiring reports still published in 2026 ([HRKatha](https://www.hrkatha.com/tag/foundit/)). Probably a mix-up with the US Monster/CareerBuilder Chapter 11. *(synthesis)*
- **Jora's footprint:** Australia-only since 2026-09-09 ([Actowiz](https://www.actowizsolutions.com/jora-data-scraping.php)) vs 24–32 countries in older profiles ([CB Insights](https://www.cbinsights.com/company/jora)). No SEEK announcement found.
- **Lagou:** bankruptcy filed in April 2026 (CB Insights) vs liquidation on 2026-05-21 (PitchBook) vs a reorganisation case dated 2026-05-15 in Chinese press ([The Paper](https://m.thepaper.cn/newsDetail_forward_33225099)). The press is the most specific.
- **Findy:** 200k users and 2,700 clients in one vendor ad, 100k and 750 in an older one ([BizReach ad](https://www.bizreach.jp/job/view/9019020/)).
- **Chinese access from abroad:** refused or challenged per one author ([Second Talent](https://www.secondtalent.com/resources/job-boards-to-hire-employees-in-china/)) vs homepages returning 200 (observed 2026-10-19). Deep pages may differ.
- **Fuzu funding:** $5.72M total (CB Insights) vs a €3.4M Series A in 2020 ([Wikipedia](https://en.wikipedia.org/wiki/Fuzu)).
- **Programathor:** listing loads but detail pages returned 500 (observed 2026-10-19): bot filtering or an outage, not resolved.

## Sources

- Brazil/LATAM: [Gupy blog](https://www.gupy.io/blog/manifesto-da-pessoa-candidata-da-gupy); [Gupy sales page](https://www.gupy.io/aumentar-atratividade-novos-talentos); [Gupy forum](https://developers.gupy.io/discuss/64cb9a32aebeb70b037dcf40); [Digibee](https://docs.digibee.com/documentation/connectors-and-triggers/connectors/industry-solutions/gupy); [Apify Gupy](https://apify.com/dadosbr/gupy-vagas.md); [Startups.com.br Gupy](https://startups.com.br/negocios/brazilian-hrtech-gupy-attracts-softbank-and-riverwood-in-93m-round/); [Vagas](https://www.vagas.com.br/vagas-de-gupy); [Betterteam Programathor](https://www.betterteam.com/br/programathor); [GeekHunter survey](https://www.geekhunter.com.br/downloads/Pesquisa_Salarial.pdf); [GeekHunter robots.txt](https://www.geekhunter.com/robots.txt); [Catraca Livre](https://catracalivre.com.br/rede/trampos/); [Diário do Comércio](https://diariodocomercio.com.br/economia/solides-lanca-portal-de-vagas-de-trabalho/); [BNE](https://www.bne.com.br/vagas-de-emprego); [Startups.com.br Revelo](https://startups.com.br/negocios/ma/no-embalo-da-ia-revelo-empilha-mas-e-quer-consolidar-na-america-latina/); [Convergência Digital](https://convergenciadigital.com.br/carreira/revelo-abre-600-vagas-e-usa-ia-para-seleo-dos-candidatos); [B2B Stack](https://www.b2bstack.com.br/product/coodesh); [Get on Board](https://www.getonbrd.com/help/que-puedo-hacer-con-la-api-de-get-on-board?lang=en); [Platzi](https://jobs.platzi.com/user-manual/get-on-board-s-api); [Cuatrecasas](https://www.cuatrecasas.com/en/global/article/redarbor-consolidates-position-in-latam-by-acquiring-majority-stake-in-infojobs-brasil-1); [Staffing Industry SEEK LATAM](https://www.staffingindustry.com/news/global-daily-news/seek-completes-sale-latin-american-job-board-businesses-0); [Gestión](https://gestion.pe/economia/empresas/bumeran-busca-ampliar-cartera-de-clientes-en-regiones-apalancado-en-nuevas-inversiones-noticia/); [TechCrunch Navent](https://techcrunch.com/?p=696550); [Torre API](https://torre.ai/es/apiforprofessionals); [Torre request](https://torre.ai/request-api); [torre-cli](https://pkg.go.dev/github.com/jjuanrivvera/torre-cli@v0.1.3)
- Europe: [Arbeitnow](https://www.arbeitnow.com/blog/job-board-api); [JOIN](https://join.com/en/features/multiposting); [ItechGuides](https://www.itechguides.com/products/join/); [TX Group](https://report.tx.group/2025/ar/en/tx-markets); [JobCloud](https://jobcloud.ch/c/en/about); [jobs.ch robots.txt](https://www.jobs.ch/robots.txt); [JobsPipe Reed](https://jobspipe.dev/blog/reed-api); [Recruiter](https://recruiter.co.uk/news/2012/04/stepstone-buys-totaljobs-group); [idibu](https://idibu.com/network/totaljobs); [StartupRise](https://startuprise.co.uk/welcome-to-the-jungle-acquired-otta/); [Brandsit](https://brandsit.pl/?p=1971322); [Mezha](https://mezha.ua/news/it-vakansiji-v-ukrajini-zrostaye-kilkist-propoziciji-dlya-data-specialistiv-rekruteriv-ta-devopsiv-303221/); [GlobeNewswire](https://www.globenewswire.com/news-release/2011/12/21/242398/0/en/Alma-Media-acquires-the-leading-online-recruitment-company-in-the-Czech-Republic.html); [LMC](https://www.lmc.eu/en/our-story); [Euronext Schibsted](https://live.euronext.com/en/products/equities/company-news/2024-10-23-schibsted-asa-schaschb-schibsted-marketplaces-advances); [Vend Q1 2025](https://vend.com/news/interim-report-q1-2025-for-schibsted-marketplaces); [Finn robots.txt](https://www.finn.no/robots.txt); [Jobindex](https://www.jobindex.dk/virksomhed/57305/robot-nordic-aps?lang=en)
- India: [Apify Naukri](https://apify.com/leadsbrary/naukri-jobs-scraper); [Cutshort](https://cutshort.io/best-platforms-to-hire-software-engineers-in-india); [People Matters](https://www.peoplematters.in/news/entrepreneurship-start-ups/info-edge-acquires-iimjobs-for-rs-8082-cr-21833); [Instahyre help](https://help.instahyre.com/en/article/explore-matching-opportunities-1s98q42/); [HRKatha](https://www.hrkatha.com/tag/foundit/); [Marketech APAC](https://marketech-apac.com/job-search-portal-monster-com-rebrands-as-foundit/); [CB Insights foundit](https://www.cbinsights.com/company/monster-worldwide); [Entrepreneur India](https://india.entrepreneur.com/news-and-trends/upgrad-acquires-internship-platform-internshala-in/503027); [Staffing Industry Internshala](https://www.staffingindustry.com/news/global-daily-news/indias-upgrad-acquires-90-stake-in-internshala); [Wellfound India](https://wellfound.com/location/india?page=4)
- East Asia: [atsoho](https://atsoho.com/blog/it-tenshoku-hikaku-site); [BizReach ad](https://www.bizreach.jp/job/view/9019020/); [Findy](https://findy-code.io/); [doda](https://doda.jp/engineer/); [seoulstart best sites](https://seoulstart.com/guides/best-job-sites-korea); [seoulstart platforms](https://seoulstart.com/guides/korean-job-platforms); [resumegeni Taiwan](https://resumegeni.com/blog/how-to-write-resume-taiwan); [104 example](https://www.104.com.tw/job/similar/8752o?page=3); [INSIDE](https://www.inside.com.tw/article/35488-cake-rebranding); [ITHome](https://www.ithome.com/0/957/960.htm); [The Paper](https://m.thepaper.cn/newsDetail_forward_33225099); [36Kr](https://www.36kr.com/p/3821852724568069); [Second Talent](https://www.secondtalent.com/resources/job-boards-to-hire-employees-in-china/)
- SE Asia, Middle East, Africa: [Jobstreet](https://my.jobstreet.com/about/news/article/seek-jobstreet-jobsdb-unify); [ITviec](https://itviec.com/employer); [ITviec example](https://itviec.com/it-jobs/principal-backend-engineer-itviec-recruitment-consulting-5728); [webcatalog TopDev](https://webcatalog.io/pl/apps/topdev); [Revelio Glints](https://www.reveliolabs.com/companies/glints/employees); [Vulcan Post](https://vulcanpost.com/911031/nodeflair-2026-singapore-tech-salaries/); [Kalibrr example](https://www.kalibrr.id/c/kalibrr-ph/jobs/215/associate-software-engineer); [ksaexpats](https://ksaexpats.com/best-job-sites-in-saudi-arabia/); [GulfTalent](https://www.gulftalent.com/uae/jobs/dubai/title/software-engineer); [100hires](https://100hires.com/uae-job-sites.html); [TechCabal](https://techcabal.com/fr/2020/10/27/jobberman-acquisition-ng-careers-roam-africa/); [Jobberman example](https://www.jobberman.com/listings/software-developer-8mpm6x); [Daily Maverick](https://www.dailymaverick.co.za/article/2025-06-24-pnet-rebrands-to-empower-south-african-jobseekers-and-recruiters-with-global-innovation.md); [PNet](https://pnet.co.za/jobs/software-developer/in-gauteng); [achisystems](https://achisystems.co.ke/directory/top-20-websites-for-jobs-in-kenya-2026/); [africaglobalfunds](https://africaglobalfunds.com/news/investors/finnishkenyan-recruitment-platform-raises-175m-from-finnfund-and-others/); [Wikipedia Fuzu](https://en.wikipedia.org/wiki/Fuzu); [WeeTracker](https://weetracker.com/2024/01/30/south-africa-hrtech-offerzen-4-3m-fundraise/)
- Canada, AU/NZ: [Semrush Canada jobs](https://nl.semrush.com/website/top/canada/jobs); [ERE](https://www.ere.net/articles/details-of-indeeds-acquisition-of-workopolis); [Manatal](https://www.manatal.com/fr/blog/niche-job-boards-canada); [Semrush CA recruitment](https://www.semrush.com/trending-websites/ca/recruitment-and-staffing); [Job Bank example](https://www.qc.jobbank.gc.ca/jobsearch/jobposting/49298197); [Staffing Industry SEEK FY2026](https://www.staffingindustry.com/news/global-daily-news/seek-reports-10-rise-in-full-year-net-revenue-while-profit-tumbles); [SEEK developer](https://developer.seek.com/); [Employment Hero](https://employmenthero.com/nz/blog/seek-is-ending-employment-hero-api-access); [MBIE](https://www.mbie.govt.nz/dmsdocument/32302-jobs-online-quarterly-report-june-2026); [Trade Me API](https://developer.trademe.co.nz/api-reference/search-methods/jobs-search); [Actowiz](https://www.actowizsolutions.com/jora-data-scraping.php); [CB Insights Jora](https://www.cbinsights.com/company/jora)
- General: [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html)
