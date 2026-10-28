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

- **[be-frank](./skills/productivity/be-frank/SKILL.md)**: a frank, researched comparison of an idea (app, product, framework, spec) against alternatives you name. You get a feature table with a source for every mark, a similarity percentage per alternative and combined, the differences that matter, the risks, and what to focus on. Claude always asks what to compare against and what the idea is for, and stops to ask questions when the idea is too vague to compare.

- **[courtroom](./skills/engineering/courtroom/SKILL.md)**: put a proposed action on trial as a motion ("fix this now", "approve this RFC", "roll this back") and get a ruling: granted, granted in part, or denied, with the order that follows. Detectives gather evidence, a prosecutor argues for the motion, a defense against, a jury of specialists votes, and a judge rules, with extra hearing rounds when the record is thin. Runs as a multi-agent [workflow](https://code.claude.com/docs/en/workflows) (about 12 to 14 agents per round). Rulings are saved to `~/.claude/courtroom/cases/`.

  > **Pro plan:** dynamic workflows are off by default. Turn on the **Dynamic workflows** row in `/config` before the first run.

- **[job-scout](./skills/productivity/job-scout/SKILL.md)**: ad-hoc research for engineering and tech job openings. Claude never guesses the kind of position: it asks whether you want an exact title, a specific role and stack, similar roles, or any engineering role, plus where and how you'd work (onsite, hybrid, remote and from where) and what kind of company. Then it pulls live postings from employer job boards (Greenhouse, Lever, Ashby and others), free remote and regional board APIs, and web search (a bundled script queries them in parallel), checks every link is still open, and returns in chat a ranked top 5 with a fit icon and the reasons for each, and the rest as one-line entries, with search details and next steps on request.

- **[stations](./skills/productivity/stations/SKILL.md)**: split your machine into *stations* (work, personal, research, ...), each with its own skills, plugins, MCP servers, settings and Claude login, so a session only carries the tools for the context it runs in. A small `claude()` shell function picks the station from the folder you start in, so a work tab and a personal tab stay logged in to different accounts at the same time. Sets up from scratch or adopts what's already on the machine, shows the full plan before changing anything, and backs up every run to `~/.agent-config-backup-<date>/` with a one-command `restore.sh`. Run it again later to catch new installs that leaked into every station.

  > **AGENTS.md:** stations keep instructions in `AGENTS.md` files: `~/AGENTS.md` for what every station shares, `<station root>/AGENTS.md` for each station. By default Claude Code skips every `AGENTS.md` once a `CLAUDE.md` exists in the start folder or above it, so one repo's `CLAUDE.md` would silently hide your station files. The skill turns on the `claude-md-and-agents-md` setting in each station so both load, and lists repos still on `CLAUDE.md` so you can rename them.
  >
  > **Not covered:** the IDE extension and desktop app don't start through your shell, so they always use the default station (`~/.claude`).

### Model-invoked

Claude reaches for these when a task matches; you can also call them by name.

- **[warm-context](./skills/productivity/warm-context/SKILL.md)**: build and load *warm-context packs*: researched domain knowledge (concepts, options, trade-offs, pitfalls) stored as indexed Markdown, so a planning session starts warm instead of from zero. Run `/rbarbaresco-skills:warm-context <topic>` to build or load a pack.

  > **Beta:** the pack format and how packs are found may still change between versions.

  Packs live in `.warm-context/` inside the folder you're working in, so a project starts with its context already there. On the first pack, the skill adds a pointer to that folder's `AGENTS.md`, so every later session there knows which packs exist. Commit `.warm-context/` to share it, or gitignore it to keep it local.

- **[uncomplicate](./skills/productivity/uncomplicate/SKILL.md)**: rewrites a dense, confusing or AI-heavy document so its reader can follow it on one read, and delivers it as a standalone HTML page (no scripts or external files, phone-friendly, printable). Structure comes before wording: conclusion first where it helps, definitions before use, duplicates merged, one term per concept. Every fact, number, qualification and citation is kept, gaps such as a missing threshold or a section that doesn't exist are flagged in place instead of filled in, and an already-clear document is left mostly alone. Editing notes sit collapsed at the end of the page. Works on human-written text too.

## License

MIT
