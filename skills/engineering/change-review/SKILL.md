---
name: change-review
disable-model-invocation: true
description: Review a code change (uncommitted work, a branch against its base, a commit or range, or a PR) through the lenses you pick (bugs, patterns, flow, history, blast radius, nitpicks) and from the viewpoint of a persona (staff engineer, on-call, security, maintainer, or free text) that decides what ranks and what gets dropped, explained to what the reader already knows (the language, the code). Every finding is grounded in evidence from the repo: file:line, commit SHA, PR number, callers. Output is one verdict, a short how-it-works note and a numbered list of plain-language findings; detail on request. On your own code it applies only the fixes you tick; on someone else's PR it drafts comments and posts only after you confirm. Use when the user runs /change-review, or asks to review a diff, a branch, a commit or a PR with a chosen focus or viewpoint.
---

# change-review

Everything after `/change-review` is the request: a target, plus optional flags anywhere in the text.

- **Target:** uncommitted changes, a branch against its base, a commit SHA or range (`a1b2c3`, `main..HEAD`), or a PR number or URL.
- `--lens bugs,flow`: lenses to run (`bugs`, `patterns`, `flow`, `history`, `blast-radius`, `nitpicks`, `default`, `all`). `default` is bugs, patterns, flow and blast radius. Skips the lens questions.
- `--persona "on-call engineer"`: whose stakes rank the findings. Free text. Skips the persona question.
- `--mine` / `--theirs`: whose code it is. Skips that question.
- `--knows "TypeScript, not this code"`: what the reader already knows. Free text. Skips the knowledge question.

Three ideas run through every step. A **lens** decides *what* gets checked. A **persona** decides *what matters*: how findings rank, which get dropped, how they're phrased. The **knowledge level** decides *how the report is written*: its vocabulary and the context it adds (see "Write to the knowledge level" in step 6). Neither persona nor knowledge level changes which checks run, so lens agents never see them.

Lens instructions live in `${CLAUDE_PLUGIN_ROOT}/skills/engineering/change-review/lenses/<lens>.md`. The read-only agent that runs them is `rbarbaresco-skills:change-review-lens`.

## 1. Resolve the target

Work out the target from the request. If none is given, pick one: uncommitted changes when `git status` is dirty, otherwise the current branch against the default branch (`git symbolic-ref --short refs/remotes/origin/HEAD`). Say which one you picked in the change summary below; the user corrects it there.

| Target | Diff | Code to read around it |
|---|---|---|
| Uncommitted | `git diff HEAD`, plus untracked files from `git status --porcelain` | working tree |
| Branch | `git diff <base>...HEAD` | working tree |
| Commit / range | `git show <sha>` / `git diff <a>..<b>` | `git show <sha>:<path>` |
| PR | `gh pr diff <n>`; metadata from `gh pr view <n> --json number,title,body,author,baseRefName,headRefOid,url` | `git fetch origin pull/<n>/head` then `git show <headRefOid>:<path>`. Never check out the PR: it would change the user's working tree. |

If the diff is empty, say so and stop.

**Change summary.** Print one or two plain sentences on what the change does and why, with the target (for example *"PR #482: moves invoice retries from the web request into a background job, so a slow provider no longer times out checkout."*). Read the intent from the PR description, linked ticket and commit messages, or from the diff when there are none. Keep it neutral; it's rewritten for the reader's knowledge level in the report. It doubles as the author intent the lens agents receive, so the user fixes a wrong one by replying, not by answering a question.

## 2. Intake

Ask everything the flags didn't answer in **one** `AskUserQuestion` call (at most 4 questions, all together, none in a second round).

1. **Which lenses?** (`multiSelect`): **Default review (Recommended)**: bugs (with security, performance and tests), patterns, flow and blast radius · **+ History**: why the touched code is shaped this way, and whether the change undoes a past decision · **+ Nitpicks**: naming, style, small cleanups · **All lenses**. Other names lenses by hand ("bugs, flow"). Picks add up: Default review plus History runs five lenses. History alone runs only history.
2. **Persona** (single select). The first option is the default, labelled with where it came from, for example *"Senior staff engineer (from ~/AGENTS.md)"*. Find it in the instruction files already loaded in this session, closest wins: the repo's `AGENTS.md` / `CLAUDE.md` if it has a role section, then the user-level file (`~/.claude/CLAUDE.md`, or `~/AGENTS.md` when loaded), then "staff engineer of this repo". Fill the other three from: **staff engineer**, **on-call engineer**, **security reviewer**, **maintainer/newcomer**, skipping whichever the default already is. Other takes free text ("a PM checking scope").
3. **Whose code?** (single select): **Mine** · **Someone else's**. Skip it, and treat the code as someone else's, when the target is a PR whose author (`author.login`) isn't the user running the skill (`gh api user --jq .login`). Otherwise recommend the option that matches the commit authors against `git config user.email`.
4. **What do you already know?** (single select). Name the main language of the change from the changed files' extensions: **Know <lang> and the code this change touches** · **Know <lang>, new to this code** · **Know this code, not <lang>** · **New to both**. Mark none as recommended: knowing a repo does not mean knowing the code a change touches. Other takes free text ("Python, not TypeScript; worked on this module last year").

No lens picked means the user skipped the question: ask once more. Don't fall back to a preset on your own, because the cost and noise of a review depends on it.

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
- the change summary from step 1, as the author intent
- the repo-rules summary from step 3
- the blame brief, for history, blast radius and flow
- this line: *"This repo's own instruction files apply to you. Read `AGENTS.md` / `CLAUDE.md` at the repo root if the summary above leaves a question open."*

Don't pass the persona, the knowledge level, or whose code it is. Those change ranking, explanation and tone, not the checks.

## 5. Merge and rank

1. **Drop** any finding without an `evidence` line a reader can open.
2. **De-duplicate:** findings on the same location with the same root cause become one finding. Keep the strongest evidence and name every lens that found it.
3. **Rank by persona.** Re-judge each severity from the persona's stakes, using the lens's severity as input, not as the answer. The same missing timeout is the top finding for an on-call engineer ("this hangs a worker at 3am"), minor for a newcomer who would rather flag that `handle()` hides three side effects, and for a staff engineer it ranks and raises whether the other callers lack it too. Final severity: 🔴 Must fix · 🟠 Should fix · 🔵 Consider.
4. **Cut** to about 6 findings: each now takes three or four lines. The persona sets the drop line: drop what this persona wouldn't raise in a real review. Count what was dropped.
5. **Verdict:** ✅ Ship (no 🔴 or 🟠) · ✋ Ship after N fixes (every 🔴 and 🟠 has a small, clear fix) · ⛔ Don't ship (any 🔴 that needs rework or a decision). The verdict never uses the severity colours, so "the orange items" can only mean findings.

## 6. Report

The list is the whole report. Detail is pulled on request, not pushed. It's a list, not a table, so any line copies cleanly into a chat, a ticket or a comment.

```
## ✋ Ship after 2 fixes   (or ✅ Ship / ⛔ Don't ship, same layout)
Change: <the step 1 summary, written to the knowledge level>

How it works: <2-3 sentences: the mechanism the change relies on, and what has to stay true for it to work>

1. 🔴 Must fix: <headline: the consequence, in plain words>
   <1-3 sentences: who it hits, and the fix>
   client.py:88 · History
2. 🟠 Should fix: <headline>
   <who it hits, and the fix>
   jobs.py:40, sync.py:12 · Blast radius

Items 1 and 2 share a cause: <the cause>.   (only when they do)

Persona: <persona> (<where it came from>) · Lenses: <picked lenses> · Knows: <knowledge level>
<N> lower findings dropped. Say "show all", or "detail N" for evidence and fix.
```

- **How it works** comes after the verdict at every knowledge level, and also when there are no findings. It names the rule the findings depend on ("every write path must call X"), so a finding reads as a broken rule, not a riddle. State only what the diff, the lens evidence or the blame brief support; where the code gives no basis for a rule, write "unverified" instead of guessing.
- Each finding opens with the consequence as a plain headline, then who it hits and the fix. `file:line` and the lens go on the last line, as a pointer. Evidence stays in "detail N".
- Ordered by severity, not by lens. Severity is written in words next to the emoji.
- When findings share a cause, close the list with one line saying which and what the cause is.
- **Change:** if a "Looked for, not found" result undercuts the change's own reason for existing (for example "no checkout caller of `send()` exists in this repo" on a change made for checkout), add it as a second line here.
- Write findings in the third person about the code ("`send()` has no timeout"), never to the reader, so step 7 can reuse the headline and the who/fix sentences. Tone follows whose code it is: **blunt** on your own code, **reviewer to peer** on someone else's.
- **Before printing**, reread each finding as someone who has not seen the diff: can they say what breaks, for whom, and what to change? If not, rewrite it.

### Write to the knowledge level

Write the whole report, Change line included, for the reader. Two independent gaps, each handled on its own:

| Reader | Headline and wording | Extra context line (beyond who/fix) |
|---|---|---|
| Knows both | In the code's own terms and the language's own idioms. No glossary. The consequence stays. | None. |
| Knows the language, new to this code | Names things by what they do, not by their repo name alone: "the `settle()` job (nightly payout)", not "`settle()`". | One line: what the component or flow is for and who calls it, the minimum to see why the finding matters. |
| Knows this code, not the language | Says the effect, not the language term: "this list is shared between calls", not "mutable default argument". | One line: what the language feature does, in terms that don't need the language. |
| New to both | Both of the above. | Up to two lines, repo context first. |

- The headline and wording are rewritten, not just annotated. Replace jargon the reader doesn't know with what it means; if the term is worth learning, give it once in parentheses, the first time it appears in the report.
- A newcomer's explanation is the *minimum* needed to act on the finding. Never a tutorial, never more than the table allows.
- Experts get fewer definitions, never fewer consequences.
- "detail N" follows the same row: the evidence stays verbatim, the surrounding explanation follows the reader.

On request:
- **"show all"**: the dropped findings in the same list shape, plus every "Looked for, not found" line from the lenses. A gap the user can't see reads as "checked and fine".
- **"detail N"**: that finding's full evidence, quoted as the lens returned it, and the suggested fix, both explained to the reader's knowledge level.

## 7. After the report

**Your own code.** Offer fixes with a multi-select `AskUserQuestion`, each fix described to the reader's knowledge level. Three findings or fewer: one option each, plus **None**. More: **All 🔴 and 🟠** · **All 🔴** · **None**, and Other takes finding numbers ("1, 3, 5"). Apply only what is ticked, in this session (the lens agents can't edit). Don't stage or commit; say which files changed.

**Someone else's code.** Never edit. If the target isn't a PR, the review ends at the report. If it is, offer to draft comments; draft only on yes.
- Comments are for the PR's author, not for the reader, so the knowledge level doesn't apply to them. A draft is the finding's headline plus its who/fix sentence: drop the severity label, the `file:line · lens` line (the comment is already anchored there) and any gloss written for the reader.
- Length follows severity so a comment never discourages reading. 🔴: one short paragraph, what breaks and why, with a link to the evidence. 🟠 / 🔵: one or two sentences. No headers, no code dumps, no restating the diff. Write a longer version only if the user asked for "detail N" and wants to post that.
- Show every draft in chat with its `file:line`, then ask once to post the whole batch. On yes, post them as one review with inline comments: `gh api repos/<owner>/<repo>/pulls/<n>/reviews --method POST --input <json>` with `event: "COMMENT"`, `commit_id: <headRefOid>`, and `comments: [{path, line, side: "RIGHT", body}]`. A comment whose line isn't in the diff goes in the review `body` instead. Nothing is ever posted without that confirmation.
