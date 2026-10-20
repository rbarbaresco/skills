# Changelog

## 0.4.0

- Add `change-review` (user-invoked): reviews a change through the lenses you pick and ranks findings for a persona you pick, with every finding grounded in `file:line`, commits, PRs or callers,, with the report written to what you say you already know about the language and the repo. It opens with a one-line summary of the change, and the report is a numbered list, so findings copy cleanly. One read-only `change-review-lens` agent per lens, in parallel. Applies only ticked fixes on your code; drafts PR comments for someone else's and posts after one confirmation.

## 0.3.0

- Add `be-frank` (user-invoked): compares an idea against alternatives you name, with a sourced feature table, similarity percentages, risks and what to focus on. Asks for what and against instead of assuming them, and stops when the idea is too vague.

## 0.2.1

- `courtroom`: role prompts and detective briefs no longer assume a specific tool stack (Datadog, Sentry, Jira, Confluence, Slack) or company; examples made generic.

## 0.2.0

- Add `stations` (user-invoked): one Claude Code config folder per context (work, personal, ...), picked from the current folder by a `claude()` shell function, with its own tools and login. Backed up per run with a `restore.sh`.

## 0.1.0

- First release: `courtroom` (user-invoked) and `warm-context` (model-invoked). Warm-context packs live in `.warm-context/` in the project folder, wired up through `AGENTS.md`; `$WARM_CONTEXT_HOME` keeps a shared library.
