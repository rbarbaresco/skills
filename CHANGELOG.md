# Changelog

## 0.6.0

- Add `uncomplicate` (model-invoked): rewrites a hard-to-follow document for its reader and delivers it as a standalone HTML page whose editing notes stay on screen and are left out of print. Reorganizes before polishing, writes for readers whose first language isn't the document's, keeps every fact and qualification, flags missing information in place instead of inventing it, and leaves already-clear documents mostly alone. A bundled stdlib Python checker allows only the tags the template uses, so it catches unescaped markup, scripts and anything loaded from the network, plus broken internal links and skipped headings; print never cuts off code or tables. Ships with six test cases for `claude plugin eval` in `evals/uncomplicate/`.

## 0.5.0

- `warm-context`: packs always go to `./.warm-context/` in the working folder, never a parent folder's library (the skill now says so). **Removed:** `$WARM_CONTEXT_HOME` and the shared library; if you set it, packs now go to `./.warm-context/` instead.

## 0.4.0

- Add `job-scout` (user-invoked): ad-hoc engineering job search. Asks for the role and how strictly to match it, the region and work mode, and the kind of company instead of assuming them (as multiple-choice questions when the agent has a question tool, numbered options otherwise); collects postings from ATS boards, free board APIs and web search (a bundled stdlib Python script queries the APIs in parallel), checks each link is open, and reports in chat a ranked top 5 with the reasons for each, and the rest as one-line entries; search details and next steps on request. Links are written as bare URLs so the list can be pasted into other chats.

## 0.3.0

- Add `be-frank` (user-invoked): compares an idea against alternatives you name, with a sourced feature table, similarity percentages, risks and what to focus on. Asks for what and against instead of assuming them, and stops when the idea is too vague.

## 0.2.1

- `courtroom`: role prompts and detective briefs no longer assume a specific tool stack (Datadog, Sentry, Jira, Confluence, Slack) or company; examples made generic.

## 0.2.0

- Add `stations` (user-invoked): one Claude Code config folder per context (work, personal, ...), picked from the current folder by a `claude()` shell function, with its own tools and login. Backed up per run with a `restore.sh`.

## 0.1.0

- First release: `courtroom` (user-invoked) and `warm-context` (model-invoked). Warm-context packs live in `.warm-context/` in the project folder, wired up through `AGENTS.md`; `$WARM_CONTEXT_HOME` keeps a shared library.
