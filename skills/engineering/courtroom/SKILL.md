---
name: courtroom
disable-model-invocation: true
description: Put a proposed action on trial as a motion — fix this, approve this, proceed with this, roll this back, defer this — and get a ruling (granted, granted in part, denied) with the order that follows. Detectives gather evidence, a prosecutor argues for the motion, a defense against, a specialist jury votes, a judge rules, with extra hearing rounds when needed. Use when the user asks "is this actually a problem", "should we fix this", "should we approve this", "is this worth tackling", "put X on trial", or "run the courtroom on X". Launches a multi-agent Workflow (~12-14 agents per round, up to 3 rounds); output is a ruling for the operator, never code, tickets, or comments.
---

# Courtroom

Everything after `/courtroom` is the case: a plain description of what is being questioned (an alert, a finding, a proposal, a ticket, a Sentry issue, an endpoint). Every case is tried as a **motion** — one imperative sentence naming the action the operator wants the court to order and its timing. The prosecutor argues for it, the defense against, and the ruling is relative to it. Optional flags anywhere in the text:

- `--motion "..."` — the motion, verbatim. Skips the motion confirmation.
- `--jury "seat, seat, seat"` — exact bench, free text per seat. Skips the bench confirmation.
- `--rounds N` — maximum hearing rounds (default 3).
- `--context "..."` — anything the operator already knows that the court should see.

Role behaviour lives in this plugin's `agents/courtroom-*.md` (one file per role; edit those to change prompts, model, or tools). The flow lives in `courtroom.js` next to this file.

## 1. Propose the motion and the bench

If both `--motion` and `--jury` were given, use them verbatim and skip to step 2.

**Motion.** Unless `--motion` was given, draft one from the case text: one imperative sentence, the action plus its timing. A symptom-shaped case ("SLO red since June") gets "Fix X now"; a proposal-shaped case gets "Approve X as written"; a direction the operator is weighing gets the direction ("Proceed with implementing X this quarter"). Also draft the flipped motion — the opposite action — so the operator can put "reject" on trial when that is the honest ask.

**Bench.** Unless `--jury` was given, read the case and propose five seats that fit it, one line of reason each. Rules of thumb: always keep **security** and **business/product impact** unless the case is clearly internal tooling with no data or customer exposure; pick the backend seat from the stack actually involved (a Go service gets "Go backend", not "Django/DRF backend"; a data pipeline gets "data engineering"); keep **SRE/observability** whenever alerts, SLOs, latency, or errors are in play; swap **API/HTTP contract** for whatever interface the case is about (a UI case gets "frontend/UX", a batch job gets "data integrity"). Then ask with `AskUserQuestion`, up to three questions in one call, skipping any the flags already answered:

1. Motion — single select. Options: **File this motion (Recommended)** with the drafted sentence as the `description` · **Flip it** with the opposite action as the `description`. Edits come through Other.
2. Bench — single select, with a `preview` showing the proposed seats and reasons. Options: **Use this bench (Recommended)** · **Plain default** (security, backend for the stack in the case, API/HTTP contract, SRE/observability, business/product impact) · **Edit seats** (the user types the change in Other).
3. Rounds — only if `--rounds` was not given: **3 (Recommended)** · **2** · **5**.

## 2. Run the trial

The user invoking this skill is the explicit opt-in for the Workflow tool. Call it with the script path and the case as `args`:

```
Workflow({
  scriptPath: "${CLAUDE_PLUGIN_ROOT}/skills/engineering/courtroom/courtroom.js",
  args: { case: "<the case text, flags removed>", motion: "<the confirmed motion>", jury: ["seat", ...], maxRounds: N, context: "<--context text or omit>" }
})
```

Pass `jury` as a real JSON array, not a string. If that call errors with "scriptPath must be a script path this tool returned, or a file you can already read..." (it will, whenever the session's working directory doesn't include this skill's directory), read `courtroom.js`'s contents and retry the same call with `script: "<those contents>"` instead of `scriptPath` — everything else (`args`, etc.) stays the same. Then wait for the completion notification; do not poll and do not start other work on the same topic.

## 3. Deliver the ruling

When the workflow returns, print in this order — ruling first, everything else after:

1. **Ruling**: the motion as filed, then decision, remedy, confidence, the judge's reasoning quoted as written (do not paraphrase it), then the dissent line.
2. **Jury**: a table — seat · ruling · remedy (one line) · confidence · one-line reasoning.
3. **Prosecution & defense thesis**: the `thesis` field from each side, quoted as written — one short paragraph each, so the operator sees each side's overall argument before the itemized detail.
4. **Grounds vs rebuttals**: each ground with its weight and the defense's counter beside it, plus each side's requested ruling and remedy.
5. **Record gaps**: every `gaps` entry from the evidence and anything in `unresolved`, verbatim. Never drop these — a gap the operator can't see reads as "checked and fine".
6. **Trial facts**: number of rounds, seats used, what the judge asked for in each round.

Write the same content to `~/.claude/courtroom/cases/<YYYY-MM-DD>-<short-slug>.md` (date from `date +%F`; slug from the case text) as the record for the operator. Put a `**Motion:**` line right under `**Case:**`. The full itemized grounds, rebuttals, and both thesis paragraphs are always in that file even when trimmed for length in the chat reply — point the operator to it rather than pasting everything inline. That file is the only artifact: never create Jira tickets, GitHub issues/PRs, Slack messages, or comments from a ruling — the operator decides what to do with the order.

If `ruling` is null or the result looks empty, read `<transcriptDir>/journal.jsonl` from the workflow result before diagnosing; it holds each agent's actual return value.
