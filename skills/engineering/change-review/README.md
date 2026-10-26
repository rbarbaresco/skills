# change-review

Review a code change the way you want it reviewed right now: pick what to look at and whose viewpoint decides what matters. Every finding points at something in the repo you can open.

**Type:** user-invoked. Run `/rbarbaresco-skills:change-review` yourself; Claude never starts it on its own.

## Why

Most review tools read like the same generic reviewer: textbook bugs, nitpicks, everything ranked from one viewpoint. They miss why the touched code is shaped the way it is (that reason usually lives in an old commit or PR), they rank the same way for an on-call engineer as for a maintainer, and they can't be told "bugs only this time".

## Usage

```
/rbarbaresco-skills:change-review PR 482
/rbarbaresco-skills:change-review my branch --lens history,blast-radius --persona "on-call engineer"
```

The target is uncommitted changes, a branch against its base, a commit or range, or a PR number or URL. Claude picks one if you leave it out, and starts with a one- or two-sentence summary of what the change does (correct it by replying). Then it asks, in a single prompt, whatever the flags didn't answer:

| Question | Flag |
|---|---|
| Which lenses? | `--lens bugs,flow` |
| Which persona? | `--persona "on-call engineer"` |
| Whose code? | `--mine` / `--theirs` (skipped when the PR author isn't you) |
| What do you already know? | `--knows "TypeScript, not this code"` |

**Lenses** decide *what* is checked: **bugs** (with security, performance and tests as sub-checks), **patterns** (does it match how this repo does things), **flow** (the path end to end), **history** (does it undo a past decision), **blast radius** (who else breaks, which sibling paths still have the problem), **nitpicks**. Two presets: **default** (bugs, patterns, flow, blast radius) and **all**.

**Personas** decide *what matters*: staff engineer, on-call engineer, security reviewer, maintainer/newcomer, or free text. The default comes from the role section of your instruction files (repo `AGENTS.md` / `CLAUDE.md` first, then your user-level one), and the picker shows where it came from.

**Knowledge level** decides *how the report is written*. Every finding states its consequence at every level; experts get fewer definitions, never fewer consequences. Not knowing the language gets effects instead of language jargon. New to the code gets components named by what they do, plus a line on what the flow is for. The finding is rewritten, not just annotated. A short *How it works* block after the verdict names the rule the findings depend on.

## What you get

```
## ✋ Ship after 2 fixes
Change: Moves webhook delivery to a background job and drops its retry loop.

How it works: `send()` posts settlement webhooks to the payment provider, and the retry loop was what survived the provider's short outages. Every caller must either retry or set a timeout, or one slow call hangs a worker.

1. 🔴 Must fix: Webhooks are lost whenever the provider has a short outage.
   The retry that PR #412 added after the March outage is removed, so one failed call is never sent again. Restore the retry in the new job.
   client.py:88 · History
2. 🟠 Should fix: Two jobs can hang forever on a slow provider.
   `jobs.py` and `sync.py` call `send()` in a loop without the timeout this change adds elsewhere. Pass the same timeout.
   jobs.py:40, sync.py:12 · Blast radius

Persona: on-call engineer (from repo AGENTS.md) · Lenses: history, blast radius · Knows: Python, new to this code
3 lower findings dropped. Say "show all", or "detail N" for evidence and fix.
```

Then:

- **Your code:** pick which findings to fix; only those are applied. Nothing is committed.
- **Someone else's PR:** never edits. On request, drafts short inline comments in chat and posts them as one review after a single confirmation.

## How it works

1. **Target and intake:** resolve the diff, summarize the change (this is also the author intent), then ask the questions above in one prompt.
2. **Context:** read the repo's `AGENTS.md` / `CLAUDE.md`. Only when history, blast radius or flow is picked: `git blame` each changed block and read the PRs behind the ones that look deliberate.
3. **Lenses:** one read-only agent per lens, in parallel (one lens runs inline). Agents can't edit files and don't know the persona, so the checks stay the same whoever is reading.
4. **Merge:** drop findings without evidence, de-duplicate, rank by persona, cut to about 6 findings, explain each to your knowledge level.

## Limitations

- **Needs a diff.** Reviewing files or folders with no change is out of scope.
- **History needs `gh`.** Without it, history and blast radius still run on git alone but can't read PR discussions.
- **Several lenses cost several agents.** Pick only what you need.
- **The report isn't saved.** Copy it from the chat if you want to keep it.

## Files

| File | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | Intake, context gathering, running lenses, ranking and the report |
| [`lenses/`](lenses/) | One instruction file per lens. Adding a lens is one new file here. |
| [`../../../agents/change-review-lens.md`](../../../agents/change-review-lens.md) | The read-only agent each lens runs in |

Design notes: [`docs/change-review-design.md`](../../../docs/change-review-design.md).
