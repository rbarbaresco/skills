# Pack format

A pack is always a folder: `<library>/<slug>/`. The slug is short and kebab-case (`pie-baking`).

## `INDEX.md` (≤ 60 lines)

```markdown
# <Topic>

> This pack is a partial sample of the domain, not its boundary. If something isn't here, it wasn't researched; that doesn't mean it doesn't exist. When the task needs it, say so and offer a gap pass (`/warm-context <slug>`).

## Scope
- **Goal:** <what the user will plan or do with this>
- **Constraints:** <...>
- **Volatility:** stable | fast-moving
- **Researched:** <YYYY-MM-DD> (updated <YYYY-MM-DD>)
- **Sources used:** web, <confirmed MCP tools>

## Coverage
- **Covered:** <topics that have files>
- **Seen but not researched:** <things that exist and came up but weren't dug into>
- **Out of scope:** <things excluded on purpose; they exist>

## Files
- [overview.md](overview.md): the core mental model; read first
- [<file>.md](<file>.md): <the question this file answers>
```

## `overview.md` (≤ 150 lines)

The mental model of the domain: what matters, how its parts relate, and the main forks in the decisions. Someone who reads only this should be able to ask good questions.

## Topic files (≤ 300 lines each, at most 8 on the first run)

One subtopic per file, named after the question it answers. Draw on these sections as they fit: concepts and vocabulary, options and trade-offs (a table when comparing more than two), rules of thumb with the reason behind each, failure modes, open questions and things that depend on context. Each file ends with a `## Sources` list.

- Link every claim to a source. Mark your own synthesis explicitly as *(synthesis)*.
- Write knowledge, not procedure: the trade-offs between shortcrust and puff pastry belong; "step 3: chill the dough" does not.
- Record disagreement between sources as disagreement.

## `CATALOG.md` line

```markdown
- [<slug>](<slug>/INDEX.md): <one-line description with the words a user would use to ask for it> (<volatility>, <YYYY-MM-DD>)
```

Keep catalog lines sorted by slug. Update the date after a gap pass or a refresh.
