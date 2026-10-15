# stations

Run separate Claude Code setups on one machine, one for each part of your life (work, personal, research, ...). Each setup is a **station**, and the folder you start `claude` in picks which one you get.

```
~/work/api        $ claude    →  station: work      (work login, work plugins, work MCP servers)
~/personal/blog   $ claude    →  station: personal  (personal login, personal skills)
~/Downloads       $ claude    →  station: default   (~/.claude, as before)
```

**Type:** user-invoked. Run `/rbarbaresco-skills:stations`; Claude never starts it on its own.

## Why

Out of the box, every Claude Code session on a machine shares one config folder (`~/.claude`). That means:

- every skill, plugin and MCP server you install shows up in every session, so a personal session sees your work tools and the other way round;
- there is one claude.ai login, so you can't keep a work account and a personal account signed in at the same time.

Stations give each context its own config folder, so each one has only the tools it needs and its own login.

## How it works

A station is three things:

| Part | Example | What it holds |
|---|---|---|
| Root folder | `~/work` | The repos that belong to this station |
| Config folder | `~/.claude-work` | Skills, agents, plugins, MCP servers, settings, history, memory and the login |
| Instructions | `~/work/AGENTS.md` | Rules for every session started under the root |

The switch is a small `claude()` shell function, installed to `~/.config/claude-stations.sh` and sourced from `~/.zshrc` or `~/.bashrc`. When you run `claude`, it finds the longest station root that contains your current folder and starts Claude Code with `CLAUDE_CONFIG_DIR` set to that station's config folder. Outside every root you get the **default station**, which is plain `~/.claude`.

Instructions live in `AGENTS.md` files and follow the folder tree, so a session loads all three levels:

1. `~/AGENTS.md`: shared by every station.
2. `<station root>/AGENTS.md`: this station only.
3. The repo's own `AGENTS.md` or `CLAUDE.md`.

## What a run does

1. **Asks** whether to start from scratch or adopt the stations already on the machine, including ones you set up by hand.
2. **Surveys** your machine without changing anything: config folders, skills, plugins, MCP servers, logins, top-level folders under `$HOME`, and anything that would override a station's login.
3. **Agrees the stations** with you: the name, root folder and purpose of each, and which one is the default.
4. **Shows a plan**: one table row per item, saying where it goes and why. Nothing changes until you confirm the table.
5. **Backs up and applies** the plan. Every action is logged to a backup folder as it happens, so even a run that fails halfway can be undone.
6. **Checks** the result: it shows what each station now carries and tells you how to log in to each new station.

Run it again later to catch anything you've installed since. The re-check lists new installs that leaked into the default station, items that don't match their station's purpose, and settings that differ between stations.

## Undoing a run

Each run writes `~/.agent-config-backup-<date>/` with a `README.md`, a `MANIFEST.tsv` that logs every action, and `restore.sh`. To undo the run:

```bash
bash ~/.agent-config-backup-<date>/restore.sh
```

Nothing is ever deleted. Moved files go back where they were, edited files get their old copy back, and anything the run created goes to an `undone/` folder.

## Limitations

- **IDE extension and desktop app:** they don't start through your shell, so they always use the default station.
- **API keys in the environment:** `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_PROFILE`, if exported, override every station's login. The survey flags them, but you have to remove them yourself.
- **Console sign-ins** stored in `~/.config/anthropic/` sit outside every config folder, so stations can't keep them apart.
- **Repos with only a `CLAUDE.md`:** by default Claude Code skips `AGENTS.md` files when a `CLAUDE.md` exists. The skill turns on the `claude-md-and-agents-md` setting so both load, and lists those repos so you can rename them. It doesn't rename them for you.
- **Plugins are installed per station,** not linked. Updating a plugin in one station doesn't update it in the others.
- **Each new station needs a `/login`** the first time you open it.
- **Settings drift:** the re-check reports `settings.json` differences between stations but doesn't sync them.

## Files

| File | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | The instructions Claude follows during a run |
| [`references/station-switch.sh`](references/station-switch.sh) | The `claude()` shell function that picks the station |
| [`references/restore.sh`](references/restore.sh) | Undoes a run from its `MANIFEST.tsv` |
