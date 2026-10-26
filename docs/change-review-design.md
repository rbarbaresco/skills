# change-review: design notes

Design decisions for `change-review`, a user-invoked code review skill for this plugin. They came out of a structured interview ("grilling") held before any code was written. Each section records the question, the decision, and the reason, so a later change can tell a deliberate choice from an accident.

Status: built in 0.4.0.

## The problem

Most code review skills read like the same generic reviewer: they hunt for textbook bugs, raise nitpicks, and rank everything from one viewpoint. They miss three things:

- **History:** why the touched code is shaped the way it is. That reason usually lives in an old commit or PR, not in a code comment.
- **The reviewer's role:** what matters to an on-call engineer is different from what matters to someone who will maintain the code.
- **What you want right now:** sometimes you want bugs only, sometimes patterns, sometimes the flow, sometimes everything.

`change-review` fixes this by asking, every run, what kind of review you want and from whose viewpoint. It also grounds every finding in evidence from the repo itself.

## Terms

| Term | Meaning |
|---|---|
| **Lens** | *What* the review looks at: bugs, flow, history, and so on. You can pick several. |
| **Persona** | *Whose stakes* decide what matters: how findings are ranked, what is worth raising, and how it is phrased. A persona never changes which checks run. |
| **Target** | The change under review: uncommitted work, a branch against its base, a commit or range, or a PR. |
| **Blame mining** | For each changed block, run `git blame` on the surrounding lines to find the commit that last touched them, then find that commit's PR (`gh pr list --search <sha>`) and read its description and review threads. |
| **Blast radius** | Everything else affected by the change: other callers of a changed function, and sibling code paths with the same problem. |

## Decisions

### Scope and invocation

| Question | Decision | Why |
|---|---|---|
| Replace the existing reviewers or add a layer on top? | Standalone skill, this plugin's own review. It overlaps with other reviewers and doesn't try to avoid that. | The goal is one review that fits how its author works, not a plug-in for someone else's. |
| User-invoked or model-invoked? | User-invoked (`disable-model-invocation: true`). | A review is something you start on purpose. |
| Code review or change review? | Change review. Reviewing files or directories with no diff is out of scope. | The useful questions ("does this undo a past decision?", "who else breaks?") need a change to compare. |
| What counts as a target? | Uncommitted changes, branch vs base (`main..HEAD`), a commit or commit range, a PR number or URL. It is free text in the prompt, and the skill asks if it is missing. | Covers self-review before a PR as well as reviewing someone else's PR. |
| Name? | `change-review`. | Bare `/code-review` already belongs to the built-in skill and to other plugins, so typing it would be ambiguous. The name also says what was decided above. |

### Intake

Every run starts with a short guided intake. Each question can be skipped with a flag:

| Question | Flag | Notes |
|---|---|---|
| Which lenses? | `--lens bugs,flow` | A multi-select picker. |
| Which persona? | `--persona "on-call"` | A menu plus free text, with a traceable default (see below). |
| Whose code? | `--mine` / `--theirs` | Skipped when the target is a PR whose author, according to `gh`, isn't the person running the skill. |
| What do you already know? | `--knows "TypeScript, not this code"` | Four options naming the change's language (knows both, new to the code, not the language, new to both) plus free text, none marked recommended: knowing a repo doesn't mean knowing the code a change touches. Like the persona it never changes which checks run, so lens agents don't see it; it decides how much each finding explains, never whether it states its consequence. |

### Lenses

1. **Bugs:** correctness, edge cases, error handling. Security, performance and tests are sub-checks here, not separate lenses, so the menu stays short enough to answer in two seconds.
2. **Patterns:** does the change match how *this* repo does things (its docs, the code next to it)?
3. **Flow:** the execution and data path end to end, including callers and side effects.
4. **History:** why the touched code is shaped the way it is, and whether the change undoes a past decision.
5. **Blast radius:** who else calls what changed, and which sibling paths are still broken.
6. **Nitpicks:** naming, style, small cleanups. Runs only when picked.
7. **Default review:** bugs, patterns, flow and blast radius, the everyday review when neither history nor nitpicks matter. Added after first use: picking four lenses one by one for the common case was slow.
8. **All.**

The picker is one multi-select question, built around the presets because `AskUserQuestion` allows four options per question: default review, + history, + nitpicks, all. Picks add up, and free text names single lenses by hand ("bugs, flow"). An earlier version split the six lenses and two presets across two questions, which read as the same question asked twice.

### Personas

The persona menu: staff engineer, on-call engineer, security reviewer, maintainer/newcomer, plus free text (for example "a PM checking scope").

How one finding ranks under different personas, taking the same missing timeout on an HTTP call:

| Persona | How it reads the finding |
|---|---|
| On-call engineer | Top finding: "this hangs a worker at 3am." |
| Maintainer/newcomer | Minor; they would rather flag that `handle()` hides three side effects. |
| Staff engineer | Ranks it, then asks whether the other callers of that client lack it too. |

**The default persona fits whoever runs the skill.** It is read from the instruction files the session already loaded, and the closest file wins:

1. The repo's `AGENTS.md` / `CLAUDE.md`, if it has a role section
2. The user-level instruction file (`~/.claude/CLAUDE.md`, or `~/AGENTS.md` when loaded)
3. Fallback: "staff engineer of this repo"

The picker shows where the default came from, for example *"Default: senior staff engineer (from ~/AGENTS.md)"*.

### Whose code

One intake question switches four things. Lenses, history and blast radius behave the same either way.

| | Your code | Someone else's code |
|---|---|---|
| Author intent | Asks you | Read from the PR description, ticket, or commits |
| Fixes | After the report, a multi-select picker lists the findings; it applies only the ones you tick | Never edits; suggests only |
| Output | Findings to act on | Comments drafted for you to post |
| Tone | Blunt | Reviewer to peer |

### Context gathering

- **Always:** read the repo's `AGENTS.md` / `CLAUDE.md` and the files they import. It is cheap and every lens benefits.
- **Only when History, Blast radius or Flow is picked:** blame mining. Blame runs for each changed block, and PRs are read only for blocks whose code looks deliberate or odd. One git call per block plus one GitHub call per PR adds up, so lenses that don't need it don't pay for it.

### Evidence

Every finding carries a source a reader can open: `file:line`, a commit SHA, a PR number, a list of callers. A finding without one is dropped, not hedged. This is the same rule as the courtroom detective's, and it keeps the History and Blast radius lenses from inventing a rationale.

### Execution

| Option | Decision |
|---|---|
| One agent works through every lens in turn | No |
| **One subagent per picked lens, in parallel; the main session merges, de-duplicates and ranks by persona** | **Yes.** Each lens gets a clean, focused context, which keeps it from drifting into a general review. A single lens runs inline. |
| A Workflow script like `courtroom` | No. There is no multi-round back-and-forth to justify it. |

Layout:

- `agents/change-review-lens.md`: one read-only agent (no Edit/Write tools, so a lens can never change code).
- `skills/engineering/change-review/lenses/<lens>.md`: one instruction file per lens, handed to the agent. The lenses differ only in their instructions, not in tools or model, so seven agent files would be copy-paste. Adding a lens is a one-file change.

### Report

The list is the whole report. Detail is pulled on request, not pushed. A first version used a table; copying a finding out of it dragged the `|` characters along, so it became a numbered list.

```
## ✋ Ship after 2 fixes
Change: Moves webhook delivery to a background job and drops its retry loop.

How it works: `send()` posts settlement webhooks to the payment provider, and the retry loop was what survived the provider's short outages. Every caller must either retry or set a timeout, or one slow call hangs a worker.

1. 🔴 Must fix: Webhooks are lost whenever the provider has a short outage.
   The retry that PR #412 added after the March outage is removed, so one failed call is never sent again. Restore the retry in the new job.
   client.py:88 · History
2. 🟠 Should fix: Two nightly jobs can hang forever on a slow provider.
   `jobs.py` and `sync.py` call `send()` in a loop without the timeout this change adds elsewhere. Pass the same timeout.
   jobs.py:40, sync.py:12 · Blast radius

Persona: on-call engineer (from repo AGENTS.md) · Lenses: history, blast radius · Knows: Python, new to this code
3 lower findings dropped. Say "show all", or "detail N" for evidence and fix.
```

- **Verdict:** ✅ Ship / ✋ Ship after fixes / ⛔ Don't ship. Not the severity colours: a 🟡 verdict beside 🟠 findings once made "the yellow items" ambiguous. A *How it works* block follows (the mechanism and what must stay true), because findings listed without it were unreadable to a reviewer who hadn't opened the diff.
- **Severity:** 🔴 Must fix, 🟠 Should fix, 🔵 Consider, in words next to the emoji. Ordered by severity, not by lens.
- **Items:** about 10 at most. A plain headline stating the consequence, 1-3 sentences on who it hits and the fix, then `file:line · lens` on the last line. Third person about the code, so a finding can be posted as it is. Findings with a shared cause get one closing line. The persona sets the drop threshold, and the footer says how many were dropped.
- **On request:** "show all" lists the dropped findings; "detail N" gives the evidence and suggested fix for one finding.

### PR comments

Only for someone else's PR, and only on opt-in. Comments are drafted in chat, and posting them as inline comments with `gh` takes one confirmation for the whole batch. They never post unasked.

Length follows severity, so a comment never discourages reading:

- 🔴: one short paragraph: what breaks and why, with a link to the evidence.
- 🟠 / 🔵: one or two sentences.
- No headers, no code dumps, no restating the diff. A longer version is only written if the reviewer asks for "detail N" and chooses to post it.

## Considered and rejected

| Idea | Why not |
|---|---|
| A per-repo rules file the skill maintains (such as `.review-rules.md`) | A new config layer for what the repo's own docs and history already answer. It would also overlap with warm-context packs, and skills here stay self-contained: no skill reads another skill's output. |
| Personas folded into lenses | They answer different questions. "Security reviewer" as a lens would just be Bugs with a slant; as a persona it changes ranking and phrasing without changing the checks. |
| Two skills, one for self-review and one for others' PRs | Only four things change between the two (see "Whose code"), so one intake question covers it. |
| Reviewing files or directories without a diff | Out of scope: this is a change review. |
| Refactoring agent instructions to share them across skills | See below. |

### Shared agent instructions

The courtroom agents share about three lines per file:

| Shared bit | Where | Size |
|---|---|---|
| `disallowedTools: Edit, Write, NotebookEdit` | all 5 | 1 frontmatter line |
| "Plain language only…" | all 5 | 1 line |
| "Read-only. Never edit files…" | all 5 | 1 line (already enforced by the frontmatter) |
| "Staff-level technologist who understands the business" | prosecutor, defense | 1 paragraph |
| "Every fact carries a source…" | detective | 1 bullet |

Sharing these would need either a runtime read of a shared file on every agent spawn, which fails silently if the path breaks, or a build step that stitches agents together from partials. Both cost more than copying three lines. `change-review-lens` copies them instead.

Revisit when a third skill with agents arrives, or when one of these lines changes and has to be edited in six places. Still to check: whether Claude Code agent files support any include mechanism. That would make the revisit cheaper but doesn't change today's decision.

## Shipping checklist

- [x] `skills/engineering/change-review/SKILL.md` with `disable-model-invocation: true`
- [x] `skills/engineering/change-review/lenses/*.md`
- [x] `agents/change-review-lens.md`
- [x] Entry in `.claude-plugin/plugin.json` `skills`
- [x] README entry under **User-invoked**
- [x] Version `0.3.0` → `0.4.0` and a `CHANGELOG.md` entry
- [x] `claude plugin validate . --strict`
