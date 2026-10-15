# courtroom

Put a decision on trial and get a ruling. You describe a proposed action, such as "fix this alert now", "approve this RFC" or "roll back this release". A team of AI agents investigates it, argues both sides, and a judge rules: **granted**, **granted in part**, or **denied**, along with what to do next.

**Type:** user-invoked. Run `/rbarbaresco-skills:courtroom <case>`; Claude never starts it on its own.

## Why

When you ask one assistant "should we do X?", you tend to get one confident answer that leans toward whatever the question implied. Courtroom splits that answer into opposing roles. One side has to make the case for the action, the other has to attack it, and specialists vote from their own angle before a judge decides. The weak spots show up in the record rather than getting smoothed over.

## Usage

```
/rbarbaresco-skills:courtroom The checkout-latency alert has fired daily since June. Is it worth fixing?
```

Before the trial starts, Claude drafts a **motion** (one sentence naming the action and its timing, for example "Fix the checkout latency alert this sprint") and a five-seat jury, then asks you to confirm or edit both.

| Flag | What it does |
|---|---|
| `--motion "..."` | Use this motion as written and skip the confirmation |
| `--jury "seat, seat, seat"` | Use exactly these jury seats |
| `--rounds N` | Maximum hearing rounds (default 3) |
| `--context "..."` | Facts you already know that the court should see |

## How a trial runs

| Step | Role | What happens |
|---|---|---|
| 1 | 4 detectives | Gather evidence in parallel, one angle each: **code** (the source and its git history), **observability** (monitors, logs, errors), **usage** (who depends on it), and **organization** (tickets, docs, past decisions). |
| 2 | Prosecutor | Argues the motion should be granted, citing the evidence. |
| 3 | Defense | Argues against it or for a narrower version, and can ask for its own investigation. |
| 4 | Jury | One agent per seat (for example security, backend, SRE, product) votes from that specialty only. |
| 5 | Judge | Reads the whole record and either rules or sends precise follow-up questions back for another round. |

Steps 4 and 5 repeat until the judge rules or the round limit is reached. On the last round the judge must rule and list anything still unresolved.

All roles are **read-only**: they can search and read, but they can't edit files. Each role's prompt, model and tools live in [`agents/courtroom-*.md`](../../../agents/) at the plugin root.

## What you get

In chat, ruling first:

1. The ruling: decision, remedy, confidence, the judge's reasoning, and any dissent.
2. A table of jury votes.
3. Each side's overall argument, then every ground with its rebuttal.
4. **Record gaps**: anything the court couldn't verify. These are never dropped, because an unchecked fact shouldn't read as "checked and fine".

The full record is saved to `~/.claude/courtroom/cases/<date>-<slug>.md`. That file is the only output. Courtroom never opens tickets, PRs or messages; acting on the ruling is up to you.

## Limitations

- **Cost:** about 12 to 14 agents per round and up to 3 rounds by default. Use it for decisions that deserve it, not quick questions.
- **Workflows must be enabled.** Courtroom runs as a Claude Code [workflow](https://code.claude.com/docs/en/workflows). On the Pro plan, turn on **Dynamic workflows** in `/config` first.
- **Evidence depends on your tools.** Detectives can only reach what your session can: the code on disk, `gh`, and whatever MCP servers you have connected (Datadog, Sentry, Jira, Slack, ...). Missing sources show up as record gaps, not as findings.
- **Engineering-leaning defaults.** The detective angles and default jury are built for software decisions. Other kinds of cases work, but edit the jury seats to fit.
- **A ruling is advice.** It is a structured argument, not a guarantee. Read the gaps before acting on it.

## Files

| File | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | How Claude drafts the motion, starts the trial and presents the ruling |
| [`courtroom.js`](courtroom.js) | The workflow script: phases, rounds, and the shape of each role's output |
| [`../../../agents/`](../../../agents/) | One file per role: detective, prosecutor, defense, juror, judge |
