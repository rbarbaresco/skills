---
name: stations
disable-model-invocation: true
description: Create, edit or delete stations (work, personal, research, ...), each a separate Claude Code config folder with its own skills, plugins, MCP servers, settings and login, picked automatically from the folder you start in. Never touches ~/.claude or any other station.
---

# Stations

A **station** is a Claude Code config folder, `~/.claude-<name>`, plus one or more **root** folders. Running `claude` anywhere under a root starts Claude Code with `CLAUDE_CONFIG_DIR` set to that folder, so the station keeps its own login, skills, agents, plugins, user MCP servers, settings, history and auto memory. A new station starts empty. `~/.claude` stays the **default station**: used outside every root, and by the IDE extension and desktop app, which don't start through the shell.

The map lives in `~/.config/claude-stations.sh`: one `<root>|<config folder>` line per root in `CLAUDE_STATIONS`, written with `$HOME`, for example `$HOME/work|$HOME/.claude-work`. A station's name is its folder's suffix. The file is a copy of `${CLAUDE_PLUGIN_ROOT}/skills/productivity/stations/references/station-switch.sh`, whose `claude()` function picks the longest matching root.

**Ground rule:** an action touches only the target station's folder, its map lines, its root's `AGENTS.md` (create, when missing) and, on the first create, one `source` line in the shell rc file. Never `~/.claude`, never another station's folder. Before editing `claude-stations.sh` or an rc file, copy it to `<file>.bak`. Leave comments and other stations' lines in the map as they are; users edit it by hand.

## Start

Read the map and list the stations: name, roots, and whether the folder has a login (`.credentials.json`). List any `~/.claude-*` folder that isn't in the map as *not managed by /stations*; no action takes it. Then ask: **create, edit or delete?**

## Create

Ask one question: **What's the station called?** The root defaults to `~/<name>`, the purpose to none. Take either from the same reply if the user gives it (`foo, root ~/code/foo, for side projects`); don't ask for them. If `~/.claude-<name>` exists or the root is already in the map, say so and ask again.

1. Create `~/.claude-<name>/settings.json` holding only `{"pluginConfigs": {"cc-plugin-agents-md@builtin": {"options": {"instructionFiles": "claude-md-and-agents-md"}}}}`, so a repo's own `CLAUDE.md` doesn't hide the `AGENTS.md` files above it.
2. Create the root and `<root>/AGENTS.md` (a heading, plus the purpose if given) only when missing. An existing `AGENTS.md` stays as it is.
3. Add the station's line to the map. When `~/.config/claude-stations.sh` doesn't exist, copy it from `station-switch.sh` first, and add `source ~/.config/claude-stations.sh` to `~/.zshrc` or `~/.bashrc` (the user's shell) unless it's already there.
4. Report in a few lines: what was created, by path; any login hazard found (`ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_PROFILE` exported in the environment or an rc file override every station's login; a `~/.config/anthropic/` folder holds a Console sign-in no station can keep apart); then: open a new terminal tab, `cd` into the root, run `claude`, `/login` once, and confirm the account in `/status`.

## Edit

Pick a station, then one of:
- **Add or remove a root:** add or remove its map line. On remove, say once that sessions saved under that root stay in this station's folder, keyed by the repo's absolute path: `claude` started there now uses another station and won't see them.
- **Rename:** move `~/.claude-<old>` to `~/.claude-<new>` and rewrite its map lines. History and login move with the folder.

## Delete

Pick a station. Show its folder's size, whether it has a login, and how many saved sessions it holds (`projects/*/*.jsonl`), and ask once. On yes: remove all its map lines, then delete the folder. Its roots and their repos stay; sessions started there now use the default station. Deleting the folder doesn't sign the account out on claude.ai.

## Guard

Refuse to edit or delete the station this session runs in (`$CLAUDE_CONFIG_DIR` is its folder): moving or deleting the folder under a live session breaks it. Ask the user to run `/stations` from another station or from a folder outside every root.
