# job-scout

Find real, open engineering and tech job postings that fit what you asked for, without Claude guessing what kind of role you meant.

**Type:** user-invoked. Run `/rbarbaresco-skills:job-scout` yourself; Claude never starts it on its own.

## Usage

```
/rbarbaresco-skills:job-scout senior backend roles, Go or Rust, remote from Portugal, scale-ups only
```

Claude needs three things, and asks for whichever is missing:

- **Role and match mode:** the role, and how strictly to match it: this exact title, this role with must-haves, similar roles, or any engineering role.
- **Where and how you'd work:** onsite or hybrid (which cities or countries), or remote and from where. Many "remote" postings are limited to one country, so this decides most of the filtering.
- **Kind of company:** startup, scale-up, big tech, enterprise, agency, public sector and so on, plus industries and exclusions.

Then it asks one round of filters (seniority, a pay floor, stack, employment type), as multiple-choice questions when the agent has a question tool and numbered options otherwise, shows the search brief and starts searching.

## What you get

- **Top 5:** each with a fit icon (🟢 strong, 🟡 likely, 🟠 stretch, ⚠️ unverified or possibly stale), location, pay, stack, posted date, the link, and why it ranks there against your brief.
- **Also open:** up to 10 more, one line each, with the reason each one isn't in the top 5.
- **Bare links** (`https://...`), so the list pastes cleanly into other chats.
- **More on request:** how the search ran, what was dropped and why, market notes, a wider search, or a saved file.

## How it works

1. **Intake:** agree the role, mode, location, company kind and filters.
2. **Plan sources:** pick employer ATS boards (Greenhouse, Lever, Ashby), free board APIs (Himalayas, Remotive, Get on Board, HN "Who is hiring?" and others) and regional boards for your region.
3. **Collect:** a bundled script queries the APIs in parallel while web searches find more postings and companies; one sweep then pulls every found company's ATS board.
4. **Verify:** a posting on its company's live ATS board counts as open; every other link is opened and checked, and postings that couldn't be checked are marked unverified.
5. **Report** in chat.

## Limitations

- **Needs web search, web fetch and Python 3** (standard library only).
- **No LinkedIn, Indeed or Glassdoor scraping.** They have no read API and block scripts; a link from them shows up only when a web search surfaces it.
- **Coverage is a sample.** Companies on other ATSs, or with no public board, can be missed.
- **The report isn't saved** unless you ask for a file.

## Files

| File | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | The instructions Claude follows for intake, sources, collecting, verifying and the report |
| [`references/sources.md`](references/sources.md) | Which job sources work without a login, how to query them, and which boards serve each region |
| [`scripts/fetch.py`](scripts/fetch.py) | Parallel fetcher for the board APIs and Greenhouse, Lever and Ashby boards |
