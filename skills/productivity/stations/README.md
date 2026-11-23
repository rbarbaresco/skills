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
| Root folder(s) | `~/work` | The repos that belong to this station; a station can have several |
| Config folder | `~/.claude-work` | Skills, agents, plugins, MCP servers, settings, history, memory and the login |
| Instructions | `~/work/AGENTS.md` | Rules for every session started under the root |

The switch is a small `claude()` shell function, installed to `~/.config/claude-stations.sh` and sourced from `~/.zshrc` or `~/.bashrc`. When you run `claude`, it finds the longest station root that contains your current folder and starts Claude Code with `CLAUDE_CONFIG_DIR` set to that station's config folder. Outside every root you get the **default station**, which is plain `~/.claude`.

Instructions live in `AGENTS.md` files and follow the folder tree, so a session loads all three levels:

1. `~/AGENTS.md`: shared by every station.
2. `<station root>/AGENTS.md`: this station only.
3. The repo's own `AGENTS.md` or `CLAUDE.md`.

## What it does

It never reads or changes `~/.claude` or any station except the one you pick. A new station starts empty: no skills, plugins or MCP servers, and its own `/login`.

| Action | What you answer | What changes |
|---|---|---|
| **Create** | the station's name; optionally a root (default `~/<name>`) and a one-line purpose | `~/.claude-<name>/` with a `settings.json`, the root and its `AGENTS.md` if missing, and the station's line in `~/.config/claude-stations.sh`. The first station also copies that file in and adds one `source` line to `~/.zshrc` or `~/.bashrc`. |
| **Edit** | which station, then a root to add or remove, or a new name | its lines in the map; a rename also moves the folder, with its login and history. A station with plugins or hooks installed can't be renamed, because they store the folder's path: create a new one and delete the old. |
| **Delete** | which station, then yes after seeing its size, login and saved sessions | its lines in the map and its folder. Its roots and repos stay; sessions there use the station whose root encloses them, or the default. |

It won't edit or delete the station you're running it from, and only acts on folders named `~/.claude-<name>`; anything else in the map is listed as not managed. Copy a skill or plugin into a new station yourself if you want it there.

## Undoing a change

Before editing `~/.config/claude-stations.sh` or your rc file, the skill copies it to `<file>.bak`. Copy that back to undo the last edit. A deleted station's folder is gone; deleting it doesn't sign the account out on claude.ai.

## Limitations

- **IDE extension and desktop app:** they don't start through your shell, so they always use the default station.
- **API keys in the environment:** `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_PROFILE`, if exported, override every station's login. Create warns about them, but you have to remove them yourself.
- **Console sign-ins** stored in `~/.config/anthropic/` sit outside every config folder, so stations can't keep them apart.
- **Repos with only a `CLAUDE.md`:** by default Claude Code skips `AGENTS.md` files when a `CLAUDE.md` exists. The skill turns on the `claude-md-and-agents-md` setting in each new station so both load.
- **Plugins are installed per station,** not linked. Updating a plugin in one station doesn't update it in the others.
- **Each new station needs a `/login`** the first time you open it.
- **Not verified on macOS:** the login is checked as a file in the config folder (Linux). How the macOS Keychain separates logins per config folder was not checked.

## Files

| File | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | The instructions Claude follows during a run |
| [`references/station-switch.sh`](references/station-switch.sh) | The `claude()` shell function that picks the station |
