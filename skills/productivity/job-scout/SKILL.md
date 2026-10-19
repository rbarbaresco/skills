---
name: job-scout
disable-model-invocation: true
description: Ad-hoc research for engineering and tech job openings from a free-text request. Asks before assuming anything about the role (exact title, a specific role and stack, similar roles, or any engineering role), the region and work mode (onsite, hybrid, remote and from where), and the kind of company. Then collects live postings from employer ATS boards, free job-board APIs and web search, checks each link is still open, and returns a ranked top 5 with reasons and the rest one line each, offering more detail on request. Use when the user runs /job-scout or asks to find, search or list engineering job openings.
compatibility: Needs web search, web fetch and Python 3 (standard library only).
---

# job-scout

Everything after `/job-scout` is the request. Act as a sourcer the user hired for one search: find real, open postings that fit what they asked for, and nothing else. A list padded with near-misses, closed links or roles the user never asked about wastes their afternoon, so a short honest list beats a long one.

Every posting in the result carries a link you opened yourself during this run, or one whose job ID is in its company's ATS board as fetched during this run. Anything you couldn't open is marked **unverified**, or dropped.

## 1. Intake

Never guess the kind of position. "Backend jobs in Berlin" could mean a senior Go role at a startup or any server-side role anywhere in Germany, and the user is the only one who knows which. Take what the request already says and ask in **two** rounds at most: the required items, then the filters. A round with nothing left to ask is skipped. Offer 2–4 concrete options per question so answering is quick, and skip any question the request already answers.

**How to ask.** If your agent has a tool that shows the user multiple-choice questions (in Claude Code, `AskUserQuestion`), use it: one call per round, one question per item, 2–4 options each, the most likely option first. These tools usually take at most 4 questions and add a free-text "Other" choice on their own, so don't add one yourself; use multi-select where several answers can apply (company kinds, adjacent roles). Role and match mode can be two separate questions; when the role isn't named at all, offer common ones (backend, frontend, platform/SRE, data) as options. Without such a tool, ask in one plain message with the options numbered per question (1a, 1b, ...) so the user can answer "1b, 2c, 3a+b".

**Required. Ask for any that are missing:**

- **Role and match mode.** What role, and how strictly to match it:
  - **Exact:** this title only ("Staff Platform Engineer").
  - **Specific:** this role with these must-haves (backend + Go + Kubernetes), any title that fits.
  - **Similar:** this role plus named or suggested adjacent ones (SRE ↔ platform ↔ DevOps). If the user picks this, propose the adjacent set and let them trim it.
  - **Generic:** any engineering or tech role. Only when the user says so.
  If the request names a role but not the mode, ask. "Data engineer" read as *exact* and as *similar* gives two very different lists.
- **Where and how they'd work.** Onsite or hybrid (which cities or countries), or remote. For remote, from where: anywhere, a country, a region, or a timezone band. "Remote" postings are often limited to one country, so this decides most of the filtering.
- **Kind of company.** For example: early startup, scale-up, big tech, enterprise or non-tech company, consultancy or agency, public sector, non-profit. Plus industry, if they care (fintech, climate, games), and exclusions (no crypto, no agencies, not company X).

**Filters, asked in round 2, one question each:**

- **Seniority:** for example junior, mid, senior, staff or principal (multi-select). Skip it if the role already names a level.
- **Pay floor:** a few ranges in the currency that fits the region, monthly or yearly as the region usually states pay, plus "No floor". State in the question that the floor is hard (postings that top out under it are dropped); a softer target goes through "Other".
- **Stack:** the languages or frameworks most common for the role, as preferences (multi-select), plus "Any stack".
- **Employment type:** local employee (for example CLT in Brazil), contractor paid by a foreign company, relocation with visa sponsorship, or either (multi-select). It decides the pay currency and which "remote" postings count.

Defaults the user can change through "Other" or in the brief: language of work any, posted or seen open in the last 30 days, a top 5 in detail plus up to 10 more one per line.

"Any" is a fine answer to a required question, but only if the user says it. Silence isn't "any". If the request is too thin to search at all ("find me a job"), say so and ask; don't run a broad search to have something to show.

**Round 2: filters.** Ask the filter questions in one call (or one numbered message).

**Then search.** Once nothing is left to ask, show the **search brief** as text (role and mode with the adjacent titles if *similar*, location and work mode, company kind, the filters, the defaults) and start searching in the same turn. Don't ask the user to confirm it or to start; they can interrupt to correct it.

## 2. Plan sources

Read `${CLAUDE_PLUGIN_ROOT}/skills/productivity/job-scout/references/sources.md`. It lists which sources work without a login, how to query them, and which boards serve each region. Pick from it based on the brief:

- **Employer ATS boards** (Greenhouse, Lever, Ashby and others) are where most tech postings start. Their public APIs need no key and give the original apply link. They work one company at a time, so you need company names first.
- **Free board APIs and feeds** cover remote, regional and community sources (Himalayas, Remotive, Get on Board, HN "Who is hiring?", and others).
- **Web search** finds both postings and companies: `site:` queries on ATS hosts are the most productive, regional boards fill gaps.

Use regional boards from the reference for the brief's region. Big boards (LinkedIn, Indeed, Glassdoor) have no read API and block scripts. You may cite a posting link from them that a search result surfaces and you could open, but don't scrape them, log in, or create accounts.

## 3. Collect

`${CLAUDE_PLUGIN_ROOT}/skills/productivity/job-scout/scripts/fetch.py` does the API work in parallel, within the per-host rate limit. Use it instead of writing your own fetch loops. Write its output to a fresh folder in your scratchpad (`$OUT` below), and build `--title` from the brief's role and match mode (for example `'(senior|staff|principal)\b.*back[\s-]?end|back[\s-]?end.*(senior|staff|principal)\b'`). Run it with `python3 -I` and that full path (shortened to `fetch.py` below).

1. **In one turn, start all of these at once:**
   - `python3 -I fetch.py boards --out $OUT --title '<regex>' '<keyword>' ...`: Himalayas, Remotive, Remote OK, Jobicy, Get on Board and the latest HN thread. A few keyword variants are enough ("backend engineer", "senior backend"). Its last line lists ATS slugs found in those postings.
   - The `site:` web searches on ATS hosts and the region's boards from the reference.
   - Searches for companies that fit the company kind and region (for example the YC directory for startups).
2. **Sweep the ATS boards once.** Collect every slug from step 1: the script's slug line, the slugs in `site:` result URLs, and your guesses for the companies you found (a bare slug tries Greenhouse, Lever and Ashby; `gh:x`, `lever:x` or `ashby:x` tries one). Then run `python3 -I fetch.py ats --out $OUT --title '<regex>' <slug> ...` once with all of them. ~50 slugs take under a minute. Run a second sweep only for a lead that turns up later.
3. **Filter against the brief** using the posting itself, not the search snippet: title and match mode, location and remote eligibility (read the fine print: "Remote (US)" is not remote from Portugal), seniority, company kind, exclusions. The full text of every posting is in `$OUT/ats.jsonl` and `$OUT/boards.jsonl` (one JSON object per line: `src`, `company`, `id`, `title`, `location`, `pay`, `posted`, `url`, `text`). Read the fine print from there with a short script or `grep`. Don't fetch those postings again.

Stop collecting once you have about twice the requested count of plausible candidates. If a source fails, the script prints `FAILED`. Note it for the closing line and move on.

## 4. Verify

A posting found in `ats.jsonl` is verified: its ID was in the company's live board during this run, which the reference calls the most reliable check. Open the rest yourself (board-only postings, web search hits). A 200 status doesn't prove a posting is open: a closed Greenhouse link redirects to the company's board, and a closed Ashby link returns an empty page. The reference lists each case. For a board posting whose company has an ATS board, look it up in the board instead (add the slug to a sweep). Then for each one:

- **Open?** Drop closed postings. Mark ones you couldn't open as **unverified** rather than dropping them silently.
- **Fresh?** Note the posted or updated date if the source gives one. Flag postings older than 60 days as possibly stale; reposting resets dates, so treat them as hints.
- **Real?** Flag scam signs (pay to apply, contact moved to chat apps, no verifiable employer) and ghost-job signs (talent-pool wording, "always hiring"). A company's own ATS board is the strongest proof the employer is real.
- **Deduplicate.** The same job shows up on several boards. Keep one row and prefer the employer's ATS link.

## 5. Report

In chat. Don't write a file or publish a page unless the user asks; then offer a dated Markdown file or an artifact page with the same content.

**Rank by fit to the whole brief**, not by match mode alone: must-haves the posting confirms, then how many preferences it meets (stack priority, pay against the floor, seniority stated), then freshness. A posting whose fine print breaks a must-have (a timezone overlap outside the user's range, pay that tops out under the floor) is dropped, not ranked low. Keep the dropped list in case the user asks for it.

Write every link as the bare full URL (`https://...`), never as `[text](url)` or `<url>`: the user copies the list into chats, where only the raw URL survives, and chat clients still make it clickable.

Put each caveat next to its posting, never in a separate section the reader has to match back by number.

Fit icons, one per posting:

- 🟢 **Strong:** every must-have is confirmed in the posting.
- 🟡 **Likely:** nothing breaks the brief, but one thing is unconfirmed (pay not listed, seniority not stated).
- 🟠 **Stretch:** fits the must-haves but misses a stated preference (secondary stack, adjacent role).
- ⚠️ goes after the icon when the posting is unverified, possibly stale, or looks like a ghost or always-open pool.

```markdown
# Job scout: <role, mode> · <where> · <company kind>

## Top 5

### 1. 🟢 <Role> · <Company> (<kind>)
<Location / work mode> · <pay, or "pay not listed"> · <main stack> · posted <date> · <ATS name>
<full URL, bare>

<One or two short paragraphs: why this ranks here against the brief (which must-haves and preferences it meets, what stands out
about the team or the work), and what to check before applying (pay band for the user's country, seniority, overlap hours).>

### 2. 🟡 ...

## Also open

- 🟠 <Role> · <Company> · <location> · <pay or "pay not listed"> · <full URL, bare> — <the one reason it's not in the top 5>
- ...

<One line offering more, for example: "Want more? How this was searched and what was dropped · market notes · a wider search · save as a file."
Add "<source> failed" when one did.>
```

Fewer than 5 good matches means fewer in the top section, not near-misses promoted to fill it. If nothing matched, say so plainly, report what was searched, and suggest which part of the brief to loosen, without loosening it yourself.
