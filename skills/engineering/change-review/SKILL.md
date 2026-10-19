---
name: change-review
disable-model-invocation: true
description: Review a code change (uncommitted work, a branch against its base, a commit or range, or a PR) through the lenses you pick (bugs, patterns, flow, history, blast radius, nitpicks) and from the viewpoint of a persona (staff engineer, on-call, security, maintainer, or free text) that decides what ranks and what gets dropped, explained to what the reader already knows (the language, the repo). Every finding is grounded in evidence from the repo: file:line, commit SHA, PR number, callers. Output is one verdict and a short numbered list; detail on request. On your own code it applies only the fixes you tick; on someone else's PR it drafts comments and posts only after you confirm. Use when the user runs /change-review, or asks to review a diff, a branch, a commit or a PR with a chosen focus or viewpoint.
---

# change-review

Everything after `/change-review` is the request: a target, plus optional flags anywhere in the text.

- **Target:** uncommitted changes, a branch against its base, a commit SHA or range (`a1b2c3`, `main..HEAD`), or a PR number or URL.
- `--lens bugs,flow`: lenses to run (`bugs`, `patterns`, `flow`, `history`, `blast-radius`, `nitpicks`, `default`, `all`). `default` is bugs, patterns, flow and blast radius. Skips the lens questions.
- `--persona "on-call engineer"`: whose stakes rank the findings. Free text. Skips the persona question.
- `--mine` / `--theirs`: whose code it is. Skips that question.
- `--knows "TypeScript, not this repo"`: what the reader already knows. Free text. Skips the knowledge question.

Three ideas run through every step. A **lens** decides *what* gets checked. A **persona** decides *what matters*: how findings rank, which get dropped, how they're phrased. The **knowledge level** decides *how much each finding explains*: a reader who doesn't know the language needs a language issue said in plain terms, and a reader new to the repo needs to be told what "this flow" is before a fix to it means anything. Neither persona nor knowledge level changes which checks run, so lens agents never see them.

Lens instructions live in `${CLAUDE_PLUGIN_ROOT}/skills/engineering/change-review/lenses/<lens>.md`. The read-only agent that runs them is `rbarbaresco-skills:change-review-lens`.

## 1. Resolve the target

Work out the target from the request. If none is given, propose one: uncommitted changes when `git status` is dirty, otherwise the current branch against the default branch (`git symbolic-ref --short refs/remotes/origin/HEAD`). Ask the user to confirm in the intake below.

| Target | Diff | Code to read around it |
|---|---|---|
| Uncommitted | `git diff HEAD`, plus untracked files from `git status --porcelain` | working tree |
| Branch | `git diff <base>...HEAD` | working tree |
| Commit / range | `git show <sha>` / `git diff <a>..<b>` | `git show <sha>:<path>` |
| PR | `gh pr diff <n>`; metadata from `gh pr view <n> --json number,title,body,author,baseRefName,headRefOid,url` | `git fetch origin pull/<n>/head` then `git show <headRefOid>:<path>`. Never check out the PR: it would change the user's working tree. |

If the diff is empty, say so and stop.

## 2. Intake

Ask everything the flags didn't answer in **one** `AskUserQuestion` call. Option lists max out at four, so lenses are split across two questions.

1. **What in the change?** (`multiSelect`): **Bugs**: correctness, edge cases, error handling; security, performance and tests as sub-checks · **Patterns**: matches how this repo does things · **Flow**: the execution and data path end to end · **Nitpicks**: naming, style, small cleanups.
2. **What around it, or a preset?** (`multiSelect`): **History**: why the touched code is shaped this way, and whether the change undoes a past decision · **Blast radius**: other callers, and sibling paths with the same problem · **Default review**: bugs, patterns, flow and blast radius, the everyday review without the history mining and nitpicks · **All lenses**: everything above.

   Picks across both questions add up: Default review plus History runs five lenses.
3. **Persona** (single select). The first option is the default, labelled with where it came from, for example *"Senior staff engineer (from ~/AGENTS.md)"*. Find it in the instruction files already loaded in this session, closest wins: the repo's `AGENTS.md` / `CLAUDE.md` if it has a role section, then the user-level file (`~/.claude/CLAUDE.md`, or `~/AGENTS.md` when loaded), then "staff engineer of this repo". Fill the other three from: **staff engineer**, **on-call engineer**, **security reviewer**, **maintainer/newcomer**, skipping whichever the default already is. Other takes free text ("a PM checking scope").
4. **Whose code?** (single select): **Mine** · **Someone else's**. Skip it, and treat the code as someone else's, when the target is a PR whose author (`author.login`) isn't the user running the skill (`gh api user --jq .login`). Otherwise recommend the option that matches the commit authors against `git config user.email`.

If the target still needs confirming, add it to the same call in place of whichever question a flag already answered, or ask it first if all four are needed.

No lens picked means the user skipped both questions: ask once more. Don't fall back to a preset on your own, because the cost and noise of a review depends on it.

Then a **second** `AskUserQuestion` call, with whichever of these weren't answered:

5. **What do you already know?** (single select). Name the main language of the change from the changed files' extensions: **Know <lang> and this repo (Recommended)** · **Know <lang>, new to this repo** · **Know this repo, not <lang>** · **New to both**. Other takes free text ("Python, not TypeScript; worked on this repo last year").
6. **Author intent**, on your own code only: what the change was meant to do. Draft it from the commit messages and branch name as the recommended option, or from the diff when there are none (uncommitted work on the default branch). Other corrects it. On someone else's code, read the intent from the PR description, the ticket it links, and the commit messages. Don't ask.

## 3. Gather context

**Always.** Read the repo's `AGENTS.md` / `CLAUDE.md` and every file they import (`@path`), plus `CONTRIBUTING.md` if present. Keep a short summary of the rules that touch the changed code for the lens prompts.

**Only when History, Blast radius or Flow is picked: blame mining.** It costs one git call per changed block plus one GitHub call per PR, so lenses that don't need it don't pay for it.

1. For each changed hunk, `git blame -L <start>,<end> --porcelain <base-or-parent> -- <file>` on the lines around it (the pre-change version) to get the commit that last touched them. A newly added file has no past to blame: blame the existing code it calls into instead, or skip it.
2. Only for blocks that look deliberate or odd (a guard, a retry, a special case, a magic number, a "don't" comment, code the change deletes), find that commit's PR (`gh pr list --state merged --search <sha>`, or the `(#N)` in the commit subject when `gh` isn't available) and read its description and review threads (`gh pr view <n> --comments`), falling back to the full commit message.
3. Write a **blame brief**: one line per block, `file:start-end → <sha> · PR #<n> or "no PR" · one-line reason quoted from the PR or commit, or "undocumented"`.

## 4. Run the lenses

One lens: run it inline. Read its lens file and follow it, with the same evidence rules as the agent below.

Two or more: spawn one `rbarbaresco-skills:change-review-lens` agent per lens, **all in the same turn** so they run in parallel. Each gets a clean, focused context, which keeps it from drifting into a general review. Each prompt carries:

- the lens file path: `${CLAUDE_PLUGIN_ROOT}/skills/engineering/change-review/lenses/<lens>.md`
- the target, the diff command and how to read the code around it (from the table in step 1), and the repo root
- the author intent
- the repo-rules summary from step 3
- the blame brief, for history, blast radius and flow
- this line: *"This repo's own instruction files apply to you. Read `AGENTS.md` / `CLAUDE.md` at the repo root if the summary above leaves a question open."*

Don't pass the persona, the knowledge level, or whose code it is. Those change ranking, explanation and tone, not the checks.

## 5. Merge and rank

1. **Drop** any finding without an `evidence` line a reader can open.
2. **De-duplicate:** findings on the same location with the same root cause become one finding. Keep the strongest evidence and name every lens that found it.
3. **Rank by persona.** Re-judge each severity from the persona's stakes, using the lens's severity as input, not as the answer. The same missing timeout is the top finding for an on-call engineer ("this hangs a worker at 3am"), minor for a newcomer who would rather flag that `handle()` hides three side effects, and for a staff engineer it ranks and raises whether the other callers lack it too. Final severity: 🔴 must fix · 🟠 should fix · 🔵 consider.
4. **Cut** to about 10 findings. The persona sets the drop line: drop what this persona wouldn't raise in a real review. Count what was dropped.
5. **Verdict:** 🟢 Ship (no 🔴 or 🟠) · 🟡 Ship after N fixes (every 🔴 and 🟠 has a small, clear fix) · 🔴 Don't ship (any 🔴 that needs rework or a decision).

## 6. Report

The list is the whole report. Detail is pulled on request, not pushed. It's a list, not a table, so any line copies cleanly into a chat, a ticket or a comment.

```
## 🟡 Ship after 2 fixes
TL;DR: <one line a reader can act on without reading further>

1. 🔴 client.py:88 · History: Removes the retry added after the #412 outage.
2. 🟠 jobs.py:40, sync.py:12 · Blast radius: Same missing timeout, not covered.
   `send()` posts settlement webhooks to the payment provider; these two jobs call it in a loop.

Persona: <persona> (<where it came from>) · Lenses: <picked lenses> · Knows: <knowledge level>
<N> lower findings dropped. Say "show all", or "detail N" for evidence and fix.
```

- One line per finding, ordered by severity, not by lens: severity, where, lens, what is wrong. Evidence belongs in "detail N", not in the line.
- **Explain to the knowledge level.** When the reader lacks the background to read a line, add one indented plain-language line under it: what the language feature does, in terms that don't need the language (for someone who doesn't know it), or what this component or flow is for in the repo (for someone new to it). Add nothing when the reader already knows both.
- **TL;DR:** if a "Looked for, not found" result undercuts the change's own reason for existing (for example "no checkout caller of `send()` exists in this repo" on a change made for checkout), say it here.
- Tone follows whose code it is: **blunt** on your own code, **reviewer to peer** on someone else's.

On request:
- **"show all"**: the dropped findings in the same list shape, plus every "Looked for, not found" line from the lenses. A gap the user can't see reads as "checked and fine".
- **"detail N"**: that finding's full evidence, quoted as the lens returned it, and the suggested fix, both explained to the reader's knowledge level.

## 7. After the report

**Your own code.** Offer fixes with a multi-select `AskUserQuestion`, each fix described to the reader's knowledge level. Three findings or fewer: one option each, plus **None**. More: **All 🔴 and 🟠** · **All 🔴** · **None**, and Other takes finding numbers ("1, 3, 5"). Apply only what is ticked, in this session (the lens agents can't edit). Don't stage or commit; say which files changed.

**Someone else's code.** Never edit. If the target isn't a PR, the review ends at the report. If it is, offer to draft comments; draft only on yes.
- Comments are for the PR's author, not for the reader, so the knowledge level doesn't apply to them.
- Length follows severity so a comment never discourages reading. 🔴: one short paragraph, what breaks and why, with a link to the evidence. 🟠 / 🔵: one or two sentences. No headers, no code dumps, no restating the diff. Write a longer version only if the user asked for "detail N" and wants to post that.
- Show every draft in chat with its `file:line`, then ask once to post the whole batch. On yes, post them as one review with inline comments: `gh api repos/<owner>/<repo>/pulls/<n>/reviews --method POST --input <json>` with `event: "COMMENT"`, `commit_id: <headRefOid>`, and `comments: [{path, line, side: "RIGHT", body}]`. A comment whose line isn't in the diff goes in the review `body` instead. Nothing is ever posted without that confirmation.
