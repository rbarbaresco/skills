# What may be collected, stored and redisplayed (US, EU, Brazil)?

> **Background research for planning, not legal advice.** Most sources are law-firm commentary or press coverage, not the judgments themselves. Primary texts were not retrieved unless stated. Consult a lawyer in each target jurisdiction before launch.

## Vocabulary

- **CFAA:** the US Computer Fraud and Abuse Act, the federal anti-hacking law.
- **Clickwrap / browsewrap:** terms you accept by clicking, versus terms that are merely linked on the page. Courts generally enforce clickwrap. Browsewrap fails unless the terms are conspicuous and the user's action clearly shows assent (*Berman v. Freedom Financial*, 9th Cir. 2022) ([Kilpatrick Townsend](https://ktslaw.com/blog/classaction/2022/4/internet-contracts-beyond-clickwrap-and-browsewrap)).
- **Sui generis database right:** an EU right, separate from copyright, that protects databases built with substantial investment (Directive 96/9/EC).
- **TDM:** text and data mining, meaning automated analysis of content. EU law allows it unless the rightholder opts out.
- **Legitimate interest:** a GDPR lawful basis that lets a business process personal data without consent, after balancing its interest against the person's rights.

## US: the line is accounts, not public pages

| Case | Holding / outcome | Login? |
|---|---|---|
| *Van Buren v. US* (2021) | Read the CFAA's "exceeds authorized access" narrowly ("gates up or down") ([Weintraub](https://www.weintraub.com/2022/04/the-continuing-battle-over-linkedin-profiles-and-the-applicability-of-the-computer-fraud-and-abuse-act/)) | — |
| *hiQ v. LinkedIn* (9th Cir. 2022; N.D. Cal. Nov 2022) | Ninth Circuit again backed hiQ on the CFAA. The district court then held the User Agreement's scraping and fake-profile bans enforceable as a contract. Dec 2022 stipulated judgment: $500,000, injunction, data destroyed ([NatLawReview](https://www.natlawreview.com/article/linkedin-s-data-scraping-battle-hiq-labs-ends-proposed-judgment); [Privacy World](https://www.privacyworld.blog/2022/12/linkedins-data-scraping-battle-with-hiq-labs-ends-with-proposed-judgment/)). Stipulated conclusions carry no precedential weight ([Proskauer](https://www.proskauer.com/insights/get-pdf/25755)) | Yes (fake profiles) |
| *Meta v. Bright Data* (N.D. Cal., 2024-01-23) | Summary judgment for Bright Data. Meta's terms did not clearly bar logged-out scraping of public data, and there was no evidence of logged-in-only data being scraped ([Lowenstein](https://www.lowenstein.com/news-insights/publications/client-alerts/meta-v-bright-data-ruling-has-important-implications-for-webscraping-activities-by-investment-advisers-im); [Pearl Cohen](https://www.pearlcohen.com/court-dismisses-data-scraping-lawsuit-against-bright-data/)) | No |
| *X Corp v. Bright Data* (N.D. Cal., May 2024) | Dismissed: no harm alleged, and claims over copying public data were preempted by the Copyright Act ([MediaPost](https://www.mediapost.com:443/publications/article/395944/judge-throws-out-xs-claims-against-data-scraper.html)). Later allowed to proceed on amended claims that scraping strained servers ([MediaPost](https://www.mediapost.com/publications/article/401510/x-corp-can-revive-scraping-battle-with-bright-dat.html)) | No |
| *LinkedIn v. Proxycurl* (2025) | Permanent injunction. Delete the data, stop access, notify customers ([LinkedIn newsroom](https://news.linkedin.com/2025/LinkedInWinsLegalBattleToProtectMemberData)) | Yes (fake accounts) |

- The sources share one thread. The losers used accounts, so they were bound by clickwrap. The winner scraped logged out. An aggregator that never logs in and never registers accounts stays on the safer side. *(synthesis)*
- The X ruling shows that server load alone can ground a claim. Polite crawl rates are a legal mitigation, not only manners. *(synthesis)*
- Freshfields doubts the Supreme Court meant the CFAA to allow scraping past technical blocks ([Freshfields](https://www.freshfields.com/en/our-thinking/blogs/a-fresh-take/data-scraping-does-it-again-102hp4o)). That is a reason not to treat getting around blocks as covered.

## robots.txt

- RFC 9309 says: "These rules are not a form of access authorization", and the protocol "is not a substitute for valid content security measures." Crawlers SHOULD NOT use a cached robots.txt for more than 24 hours ([RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html)).
- So ignoring it is not hacking. But honoring it is the clear norm, it weakens a claim of bad faith, and in the EU it is the leading candidate for a valid machine-readable opt-out from data mining. *(synthesis)*
- An Amsterdam court (*DPG Media v. HowardsHome*, late 2024) held that an opt-out need not follow one standard, but must be practically detectable and processable by machines ([Freshfields](https://technologyquotient.freshfields.com/post/102mebl/ai-training-copyright-part-2-text-and-data-mining-under-court-scrutiny)).
- No US court holding on robots.txt was retrieved.

## Copyright: facts vs expression

- **Facts are not copyrightable:** title, company, location, salary, skills and apply URL. The free-text description can be. The lowest-risk pattern is to store and show structured facts plus at most a short snippet, and link out to the original. *(synthesis; *Feist v. Rural* (1991) is the standard authority, but no page for it was retrieved)*
- **"Hot news" misappropriation** (*NBA v. Motorola*, 1997) needs costly, time-sensitive information, free-riding, direct competition and a threat to the incentive to produce it ([DMLP](https://www.dmlp.org/print/5785)). *Barclays v. Theflyonthewall* (2d Cir. 2011) held the claim preempted ([EFF](https://www.eff.org/cases/barclays-v-theflyonthewall-com)). In theory a rival job board could plead it, but it is unlikely to succeed. *(synthesis)*
- No case was found specifically on copyright in job-ad text, in any jurisdiction.

## EU: the database right is the main risk

- ***Innoweb v. Wegener*** (C-202/12, 2013): a car-ads meta-search engine that translated user queries into a rival site's search engine in real time re-utilised a substantial part of that database ([IPKat](https://ipkitten.blogspot.com/2013/12/stepping-on-gaspedaal-cjeu-rules-on-re.html); [SCL](https://www.scl.org/2984-database-right-innoweb-v-wegener-cjeu-judgment/)).
- ***CV-Online Latvia v. Melons*** (C-762/19, 2021-06-03): a job-ads case. KurDarbs.lv, a job-ad search engine that links to original postings, was sued by cv.lv ([ICLR](https://www.iclr.co.uk/document/2021002793/casereport_ce1c572d-0507-423f-bdb7-eacfa75df132/html); [WIPO Lex](https://www.wipo.int/wipolex/es/text/596504)). Husovec says the judgment "significantly alters the previous case law on the infringement test" ([Husovec](https://husovec.eu/2021/06/cjeu-redefines-sui-generis-database-right/)).
  - **Warning: the holding below is UNVERIFIED against the judgment text.** It comes from background knowledge, because the curia and EUR-Lex pages returned blank. Check it against the [WIPO Lex text](https://www.wipo.int/wipolex/es/text/596504). The reading: indexing and searching a job site's database is extraction and re-utilisation, but it infringes only if it puts at risk the maker's chance to recoup its substantial investment. National courts must weigh that against users' and competitors' interest in access to information.
- ***Ryanair v. PR Aviation*** (C-30/14, 2015): where the Directive does not protect a database, the owner can still restrict use by contract, through terms that ban scraping ([Travolution](https://www.travolution.com/news/travel-sectors/tour-operators/eu-court-of-justice-ruling-backs-ryanair-in-screen-scraper-dispute/)).
- **What follows for design** *(synthesis)*:
  - Linking out and copying little helps under a harm test.
  - Mirroring a whole board, or live querying a board (the Innoweb pattern), is the riskiest EU design.
  - Employers' own ATS boards are weaker ground for a database-right claim than costly board databases.
  - Clickwrap sites can still bind by contract (*Ryanair*).
- **TDM opt-outs** (DSM Directive Art. 4) are a split picture:
  - LG Hamburg suggested in dicta that a natural-language reservation can count.
  - OLG Hamburg found a reservation in a site's terms of use not machine-readable enough. A BGH appeal was admitted ([Open Future](https://openfuture.eu/blog/laion-round-2-machine-readable-but-still-not-actionable/); [Kluwer](https://legalblogs.wolterskluwer.com/copyright-blog/kneschke-vs-laion-landmark-ruling-on-tdm-exceptions-for-ai-training-data-part-2/)).
  - A Danish court (Oct 2025) accepted a ban in an HTML policy ([Freshfields](https://technologyquotient.freshfields.com/post/102mebl/ai-training-copyright-part-2-text-and-data-mining-under-court-scrutiny)).
  - TDM matters most for the research skill and any ML processing. A plain aggregator turns mainly on the database right. *(synthesis)*

## Personal data: GDPR and LGPD

- A recruiter's name, email or phone in a posting is personal data. Being public does not remove GDPR or LGPD duties. *(synthesis from sources below)*
- **EDPB Opinion 28/2024** accepts legitimate interest for scraping if the three-part test is met. On necessity, commentators read it as favouring narrow collection criteria ([Slaughter and May](https://thelens.slaughterandmay.com/post/102nequ/caught-in-the-web-edpb-guidelines-on-scraping-for-generative-ai)). Draft **Guidelines 03/2026** on scraping are in consultation until 2026-10-30 ([SKW Schwarz](https://www.skwschwarz.de/en/news/ki-flash-edpb-guidelines-web-scraping-ai); [Bratby](https://bratby.law/edpb-web-scraping-generative-ai-guidelines/)).
- **Regulators disagree.** The Dutch DPA is restrictive and treats legitimate interest for scraping as hard to establish. France's CNIL holds that a commercial aim does not by itself rule it out ([IAPP](https://iapp.org/news/a/the-state-of-web-scraping-in-the-eu); [Clifford Chance](https://www.cliffordchance.com/insights/resources/blogs/talking-tech/en/articles/2025/06/web-scraping-for-ai-development--the-cnil-builds-on-edpb-guidanc.html)).
- **Brazil, LGPD Art. 7:**
  - §4 waives consent for data made manifestly public.
  - §3 requires respecting the purpose, good faith and public interest that justified making it public.
  - §6 keeps the controller's other duties.
  - §7 allows new purposes only if they are legitimate and specific.
  - [Modelo Inicial](https://modeloinicial.com.br/lei/LGPD/lei-geral-protecao-dados-pessoais/art-7,inc-X); [Migalhas](https://www.migalhas.com.br/depeso/293745/a-excecao-dos-dados-pessoais-tornados-manifestamente-publicos-pelo-titular-na-lgpd)
  - Scraping still needs a legal basis and the Art. 6 principles ([Monitor Mercantil](https://monitormercantil.com.br/data-scraping-e-a-responsabilidade-do-controlador/)). A community newsletter says the ANPD issued a first scraping fine. This is **unverified** ([TabNews](https://www.tabnews.com.br/NewsletterOficial/anpd-alerta-que-web-scraping-de-dados-pessoais-viola-lgpd)).
- **Reading** *(synthesis)*:
  - Showing a recruiter's contact for the same job, with a link back, arguably matches the purpose it was published for.
  - Harvesting recruiter contacts into a searchable directory or reselling them does not. That is the Proxycurl pattern.
  - The simplest design keeps no recruiter personal data at all, only the company and the apply URL.
  - GDPR Art. 14, the duty to inform people whose data was obtained indirectly, applies to scrapers. That is standard doctrine; no source was retrieved.

## Platform norms: Google for Jobs as the de facto standard

- **Rules:**
  - Markup only on single-job pages.
  - Canonical URLs on duplicate copies.
  - No expired jobs; late removal "may result in a manual action".
  - No login wall.
  - No "job postings on behalf of an organization or company without authorization".
  - [Google Search Central](https://developers.google.com/search/docs/appearance/structured-data/job-posting)
- **Tension:** "without authorization" argues against marking up scraped jobs, while the ban on "incomplete descriptions" pushes towards copying full text, which is the riskiest copyright and database pattern. The resolution consistent with both: don't emit JobPosting markup for scraped jobs, and let the employer's page win in Google. *(synthesis)*
- Common norms the sources did not document: "via X" attribution, `rel="nofollow"` or `rel="sponsored"` on outbound links, and a published takedown or opt-out contact. Source-specific terms (Remotive, Himalayas, Adzuna) are in [aggregator-and-board-apis.md](aggregator-and-board-apis.md).

## Disagreements

- **TDM opt-out form:** LG Hamburg (natural language may count) vs OLG Hamburg (terms of use not machine-readable enough) vs Amsterdam (must be machine-processable) vs Denmark (HTML policy accepted).
- **Legitimate interest for scraping:** Dutch DPA restrictive, CNIL permissive.
- **Reach of hiQ after Van Buren:** Freshfields doubts it covers scraping past technical blocks.
- **Meta's dismissal of its last claim:** Bright Data calls it a concession, not a settlement. That is a party's own framing ([Calcalist](https://www.calcalistech.com/ctechnews/article/h1zshv53p)).
- **Ryanair:** Lambrecht doubts it clarifies contractual protection of databases ([UCLouvain](https://research.dial.uclouvain.be/bitstreams/3582a677-d172-4ab5-aaf6-60ef686acc48/download)).
- **Draft EDPB Guidelines 03/2026 date:** July 7 vs July 8, 2026.

## Open questions

- *CV-Online* holding: verify against the judgment.
- UK position after Brexit: the database right, the non-commercial-only TDM exception (CDPA s29A) and the ICO's view on scraping. Not researched.
- Current status of *X v. Bright Data*; outcome of the BGH appeal in *Kneschke v. LAION*.
- Trespass to chattels (*eBay v. Bidder's Edge*, *Intel v. Hamidi*), the CCPA's "publicly available" exemption, and Clearview AI fines. Not researched.

## Sources

- [Weintraub](https://www.weintraub.com/2022/04/the-continuing-battle-over-linkedin-profiles-and-the-applicability-of-the-computer-fraud-and-abuse-act/); [Apify hiQ blog](https://blog.apify.com/hiq-v-linkedin); [Freshfields on hiQ](https://www.freshfields.com/en/our-thinking/blogs/a-fresh-take/data-scraping-does-it-again-102hp4o)
- [NatLawReview hiQ](https://www.natlawreview.com/article/linkedin-s-data-scraping-battle-hiq-labs-ends-proposed-judgment); [Privacy World](https://www.privacyworld.blog/2022/12/linkedins-data-scraping-battle-with-hiq-labs-ends-with-proposed-judgment/); [Proskauer](https://www.proskauer.com/insights/get-pdf/25755)
- [Lowenstein](https://www.lowenstein.com/news-insights/publications/client-alerts/meta-v-bright-data-ruling-has-important-implications-for-webscraping-activities-by-investment-advisers-im); [Pearl Cohen](https://www.pearlcohen.com/court-dismisses-data-scraping-lawsuit-against-bright-data/); [Calcalist](https://www.calcalistech.com/ctechnews/article/h1zshv53p)
- [MediaPost X v. Bright Data (2024)](https://www.mediapost.com:443/publications/article/395944/judge-throws-out-xs-claims-against-data-scraper.html); [MediaPost revived claims](https://www.mediapost.com/publications/article/401510/x-corp-can-revive-scraping-battle-with-bright-dat.html)
- [LinkedIn newsroom (Proxycurl)](https://news.linkedin.com/2025/LinkedInWinsLegalBattleToProtectMemberData)
- [Kilpatrick Townsend](https://ktslaw.com/blog/classaction/2022/4/internet-contracts-beyond-clickwrap-and-browsewrap)
- [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html); [Freshfields TDM](https://technologyquotient.freshfields.com/post/102mebl/ai-training-copyright-part-2-text-and-data-mining-under-court-scrutiny)
- [DMLP hot news](https://www.dmlp.org/print/5785); [EFF Barclays](https://www.eff.org/cases/barclays-v-theflyonthewall-com)
- [ICLR CV-Online](https://www.iclr.co.uk/document/2021002793/casereport_ce1c572d-0507-423f-bdb7-eacfa75df132/html); [WIPO Lex](https://www.wipo.int/wipolex/es/text/596504); [Husovec](https://husovec.eu/2021/06/cjeu-redefines-sui-generis-database-right/)
- [IPKat Innoweb](https://ipkitten.blogspot.com/2013/12/stepping-on-gaspedaal-cjeu-rules-on-re.html); [SCL](https://www.scl.org/2984-database-right-innoweb-v-wegener-cjeu-judgment/); [Travolution Ryanair](https://www.travolution.com/news/travel-sectors/tour-operators/eu-court-of-justice-ruling-backs-ryanair-in-screen-scraper-dispute/); [UCLouvain](https://research.dial.uclouvain.be/bitstreams/3582a677-d172-4ab5-aaf6-60ef686acc48/download)
- [Open Future](https://openfuture.eu/blog/laion-round-2-machine-readable-but-still-not-actionable/); [Kluwer Copyright Blog](https://legalblogs.wolterskluwer.com/copyright-blog/kneschke-vs-laion-landmark-ruling-on-tdm-exceptions-for-ai-training-data-part-2/)
- [Slaughter and May](https://thelens.slaughterandmay.com/post/102nequ/caught-in-the-web-edpb-guidelines-on-scraping-for-generative-ai); [SKW Schwarz](https://www.skwschwarz.de/en/news/ki-flash-edpb-guidelines-web-scraping-ai); [Bratby](https://bratby.law/edpb-web-scraping-generative-ai-guidelines/); [IAPP](https://iapp.org/news/a/the-state-of-web-scraping-in-the-eu); [Clifford Chance](https://www.cliffordchance.com/insights/resources/blogs/talking-tech/en/articles/2025/06/web-scraping-for-ai-development--the-cnil-builds-on-edpb-guidanc.html)
- [Modelo Inicial LGPD](https://modeloinicial.com.br/lei/LGPD/lei-geral-protecao-dados-pessoais/art-7,inc-X); [Migalhas](https://www.migalhas.com.br/depeso/293745/a-excecao-dos-dados-pessoais-tornados-manifestamente-publicos-pelo-titular-na-lgpd); [Monitor Mercantil](https://monitormercantil.com.br/data-scraping-e-a-responsabilidade-do-controlador/); [TabNews (unverified)](https://www.tabnews.com.br/NewsletterOficial/anpd-alerta-que-web-scraping-de-dados-pessoais-viola-lgpd)
- [Google Search Central: job posting](https://developers.google.com/search/docs/appearance/structured-data/job-posting)
