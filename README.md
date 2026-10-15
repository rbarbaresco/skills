# Skills

The Claude Code skills I use every day, packaged as a plugin you install once and keep up to date.

## Installation

```bash
claude plugin install rbarbaresco-skills --marketplace rbarbaresco/skills
```

Or, from inside a session:

```
/plugin install rbarbaresco-skills --marketplace rbarbaresco/skills
```

On Claude Code older than 2.1.275, add the marketplace first, then install:

```bash
claude plugin marketplace add rbarbaresco/skills
claude plugin install rbarbaresco-skills@rbarbaresco
```

Skills run as `/rbarbaresco-skills:<name>`.

## Skills

Skills are grouped into folders under `skills/`: `engineering/` for code and production work, `productivity/` for everything around it.

### User-invoked

You start these yourself; Claude never triggers them on its own.

- **[courtroom](./skills/engineering/courtroom/SKILL.md)**: put a proposed action on trial as a motion ("fix this now", "approve this RFC", "roll this back") and get a ruling: granted, granted in part, or denied, with the order that follows. Detectives gather evidence, a prosecutor argues for the motion, a defense against, a jury of specialists votes, and a judge rules, with extra hearing rounds when the record is thin. Runs as a multi-agent [workflow](https://code.claude.com/docs/en/workflows) (about 12 to 14 agents per round). Rulings are saved to `~/.claude/courtroom/cases/`.

  > **Pro plan:** dynamic workflows are off by default. Turn on the **Dynamic workflows** row in `/config` before the first run.

### Model-invoked

Claude reaches for these when a task matches; you can also call them by name.

- **[warm-context](./skills/productivity/warm-context/SKILL.md)**: build and load *warm-context packs*: researched domain knowledge (concepts, options, trade-offs, pitfalls) stored as indexed Markdown, so a planning session starts warm instead of from zero. Run `/rbarbaresco-skills:warm-context <topic>` to build or load a pack.

  Packs live in `.warm-context/` inside the folder you're working in, so a project starts with its context already there. On the first pack, the skill adds a pointer to that folder's `AGENTS.md`, so every later session there knows which packs exist. Commit `.warm-context/` to share it, or gitignore it to keep it local. To keep one shared library across projects instead, set `$WARM_CONTEXT_HOME` (for example to `~/warm-context`) and import its `CATALOG.md` from your `~/.claude/CLAUDE.md`.

## License

MIT
