---
name: stations
disable-model-invocation: true
description: Create, edit or delete stations (work, personal, research, ...), each a separate Claude Code config folder with its own skills, plugins, MCP servers, settings and login, picked automatically from the folder you start in. Never touches ~/.claude or any other station.
---

# Stations

A **station** is a Claude Code config folder, `~/.claude-<name>`, plus one or more **root** folders. Running `claude` anywhere under a root starts Claude Code with `CLAUDE_CONFIG_DIR` set to that folder, so the station keeps its own login, skills, agents, plugins, user MCP servers, settings, history and auto memory. A new station starts empty. `~/.claude` stays the **default station**: used outside every root, and by the IDE extension and desktop app, which don't start through the shell.

The map lives in `~/.config/claude-stations.sh`: one `<root>|<config folder>` line per root in `CLAUDE_STATIONS`. The file is a copy of `${CLAUDE_PLUGIN_ROOT}/skills/productivity/stations/references/station-switch.sh`, whose `claude()` function picks the longest matching root, so a nested root wins over the one around it.

**Ground rules**
- An action writes only the target station's folder, its map lines, its root's `AGENTS.md` (create, when missing) and the `source` line in the shell rc file. Never `~/.claude`, never another station's folder.
- A name is `[a-z0-9-]+`. A station is **managed** only when its folder resolves to exactly `$HOME/.claude-<name>` with such a name. List any other map line or `~/.claude-*` folder as *not managed by /stations* and never act on it. That covers a line pointing at `~/.claude`. Commands act on `$HOME/.claude-<name>` built from the name, never on the string from the map, and refuse when that path is a symlink.
- Users edit the map by hand, so lines may use `$HOME`, an absolute path or a trailing `/`. Read the map by sourcing it in a subshell (`bash -c '. ~/.config/claude-stations.sh; printf "%s\n" "$CLAUDE_STATIONS"'`) and compare expanded paths with the trailing `/` dropped. Write new lines as `$HOME/<path>|$HOME/.claude-<name>`, with no `~` and no trailing `/`. Leave comments and other lines as they are.
- Before editing `claude-stations.sh` or an rc file, copy it to `<file>.bak`.
- A root is never `~` or `/`. Either one would take over every session that now uses the default station.

## Start

Read the map and list the managed stations: name, roots, and whether the folder has a login (`.credentials.json`). List the unmanaged ones after them. Then ask: **create, edit or delete?**

## Create

Ask one question: **What's the station called?** The root defaults to `~/<name>`, the purpose to none. Take either from the same reply if the user gives it (`foo, root ~/code/foo, for side projects`); don't ask for them. Ask again if the name breaks the name rule, `~/.claude-<name>` exists, or the root is already in the map. If the root sits inside another station's root, or contains one, say that sessions there will move to the new, empty station, and ask once.

1. Create `~/.claude-<name>/settings.json` holding only `{"pluginConfigs": {"cc-plugin-agents-md@builtin": {"options": {"instructionFiles": "claude-md-and-agents-md"}}}}`, so a repo's own `CLAUDE.md` doesn't hide the `AGENTS.md` files above it.
2. Create the root and `<root>/AGENTS.md` (a heading, plus the purpose if given) only when missing. An existing `AGENTS.md` stays as it is.
3. Add the station's line to the map. When `~/.config/claude-stations.sh` doesn't exist, copy it from `station-switch.sh` first. Add `source ~/.config/claude-stations.sh` to `~/.zshrc` or `~/.bashrc` (the user's shell) unless the file already sources it.
4. Report in a few lines: what was created, by path; any login hazard found (`ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_PROFILE` exported in the environment or an rc file override every station's login; a `~/.config/anthropic/` folder holds a Console sign-in no station can keep apart); then: open a new terminal tab, `cd` into the root, run `claude`, `/login` once, and confirm the account in `/status`.

## Edit

Pick a managed station, then one of:
- **Add a root:** the same root checks as Create, then add its map line.
- **Remove a root:** refuse when it's the station's last root and point to Delete. Otherwise remove the line, and say once that sessions saved under that root stay in this station's folder, keyed by the repo's absolute path: `claude` started there now uses another station and won't see them.
- **Rename:** the new name follows the name rule, and neither `~/.claude-<new>` nor a map line for it may exist. Refuse when `.claude-<old>`, written in any form (`~`, `$HOME` or absolute), appears in the folder's `plugins/`, `settings.json`, `settings.local.json` or `.claude.json`. Installed plugins, hooks and MCP servers that point into the folder would be left pointing at a folder that's gone. Suggest a new station plus Delete instead. Otherwise move `~/.claude-<old>` to `~/.claude-<new>` and rewrite its map lines. History moves with the folder, and so does the login on Linux; on macOS the user may need to `/login` again. The roots stay where they are.

## Delete

Pick a managed station. Show its folder's size, whether it has a login, and how many saved sessions it holds (`projects/*/*.jsonl`). Ask the user to close any other session running in it, then ask once. On yes: remove all its map lines and read the map again. Delete the folder only when no line still resolves to it. Its roots and their repos stay; sessions started there now use the station whose root encloses them, or the default. Deleting the folder doesn't sign the account out on claude.ai.

## Guard

Refuse to edit or delete the station this session runs in (`$CLAUDE_CONFIG_DIR` is its folder): moving or deleting the folder under a live session breaks it. Ask the user to run `/stations` from another station or from a folder outside every root.
