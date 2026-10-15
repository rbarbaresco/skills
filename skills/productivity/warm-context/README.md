# warm-context

Research a subject once and keep what was learned, so later planning sessions start with the background already in place instead of from zero.

> **Beta:** the pack format and how packs are found may still change between versions.

**Type:** model-invoked. Claude uses it when a task matches a pack you already have. You can also run `/rbarbaresco-skills:warm-context <topic>` yourself.

## What a pack is

A **pack** is a folder of researched notes on one subject: the key concepts, the options and what each one trades off, rules of thumb, and common failures. It holds knowledge about the subject, not a step-by-step plan.

For example, a pack on "baking pies" covers pastry science, pie families, fillings and why pies fail. It leaves out any single recipe. You plan the recipe later, in a session that has already loaded the pack.

## Usage

```
/rbarbaresco-skills:warm-context postgres partitioning
```

- **No pack on the topic yet:** Claude asks 3 to 5 short questions (your goal, constraints, what to leave out, whether the topic changes fast, and which connected tools it may use), researches it, and writes the pack. Answer "just go" to let Claude pick reasonable answers.
- **A pack already matches:** Claude loads it, tells you if it's out of date, and names any part of your task the pack doesn't cover. It offers a small research pass to fill those gaps.

## How it works

1. **Match** the topic against the catalog of existing packs, by description as well as name.
2. **Intake:** agree the scope and plan up to 8 subtopics.
3. **Research** each subtopic. Claude prefers primary sources (official docs, specs, practitioners) and records a source URL for every claim. Where sources disagree, both positions are kept. Things it came across but didn't dig into are listed as *seen but not researched*, so the pack shows its own limits.
4. **Write** the pack and add a line for it to the catalog.

## Where packs live

By default, packs are written to `.warm-context/` in the folder you're working in:

```
.warm-context/
├── CATALOG.md          one line per pack
└── postgres-partitioning/
    ├── INDEX.md        scope, coverage, research date, file list
    ├── overview.md     the short version
    └── <topic>.md      one file per subtopic
```

The first time it writes a pack, the skill adds a short section to that folder's `AGENTS.md` that points to the catalog, so every later session there knows which packs exist. Commit `.warm-context/` to share packs with your team, or gitignore it to keep them local.

To keep one library for all your projects, set `$WARM_CONTEXT_HOME` (for example `~/warm-context`) and import its `CATALOG.md` from `~/.claude/CLAUDE.md`.

## Limitations

- **Needs web search.** Research also goes faster with subagents or a deep-research skill, but those are optional.
- **A pack is a sample, not the whole subject.** Treat anything missing from a pack as unresearched, not as nonexistent.
- **Packs go stale.** For topics marked fast-moving, Claude warns you when a pack is more than 6 months old and offers a refresh. Stable topics are never flagged.
- **Size caps keep packs readable:** at most 8 topic files on the first run and about 300 lines each. Deep topics need follow-up gap passes.
- **Only web sources and the tools you approve** at intake. Private documents are left out unless a connected tool can reach them and you allow it.

## Files

| File | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | The instructions Claude follows to match, load, research and write packs |
| [`references/research-loop.md`](references/research-loop.md) | How each subtopic gets researched |
| [`references/pack-format.md`](references/pack-format.md) | The layout and size limits of a pack |
