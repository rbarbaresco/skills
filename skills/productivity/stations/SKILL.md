---
name: stations
disable-model-invocation: true
description: Split one workstation into stations (work, personal, research, ...), each with its own Claude Code skills, plugins, MCP servers, settings and login, picked automatically from the folder you start in. Sets up from scratch, adopts what's already on the machine, and re-checks later. Every run is backed up with a one-command restore.
---

# Stations

A **station** is an office: a root folder, a one-line purpose, and its own Claude Code config folder (`CLAUDE_CONFIG_DIR`). Walking into the folder switches the whole office: skills, agents, rules, plugins, user MCP servers, settings, history, auto memory, and the claude.ai login. Separate logins mean a work account and a personal account run side by side in different terminal tabs.

What the office carries and what it doesn't:
- **Tools** live in the config folder. Claude Code reads project skills and `.claude/settings.json` only up to the repo root, so a `.claude/` folder at a station root never reaches the repos inside it. That's why stations switch config folders, not project folders.
- **Instructions** follow the folder tree: every `AGENTS.md` from the start folder up to `/` loads. The shared core lives in `~/AGENTS.md`, station rules in `<root>/AGENTS.md`, repo rules in the repo.
- `~/.claude` stays the **default station**, used outside every station root, and by the IDE extension and desktop app, which don't start through the shell.

Two files ship with this skill:
- `${CLAUDE_PLUGIN_ROOT}/skills/productivity/stations/references/station-switch.sh`: the `claude()` shell function that picks the config folder from `$PWD`.
- `${CLAUDE_PLUGIN_ROOT}/skills/productivity/stations/references/restore.sh`: undoes a run from its `MANIFEST.tsv`. Its header defines the manifest format.

## 1. Branch

Ask first, before reading anything: **start from scratch, or work with the stations already on this machine?** Stations already on the machine include ones set up by hand, without this skill. A machine where `~/.config/claude-stations.sh` exists has been through `/stations` before: the "existing" path then doubles as the **re-check** (step 6).

## 2. Survey

Read-only. Collect:
- **Config folders:** `~/.claude`, every `~/.claude-*`, and every `CLAUDE_CONFIG_DIR` set in `~/.zshrc`, `~/.bashrc`, `~/.profile`, or an alias or function there.
- **Per config folder:** loose skills in `skills/` (name and description from frontmatter, and whether it's a symlink), `agents/`, `rules/`, `CLAUDE.md`, `settings.json` (`enabledPlugins`, the `instructionFiles` setting), installed plugins (`CLAUDE_CONFIG_DIR=<dir> claude plugin list`), user MCP servers (`CLAUDE_CONFIG_DIR=<dir> claude mcp list`), whether `.credentials.json` exists, and the `projects/<key>/` folders (a key is the absolute project path with every `/` turned into `-`).
- **Folders:** top-level folders under `$HOME` that hold git repos, grouped by git remote owner (an organisation usually means an employer). Also `AGENTS.md`, `CLAUDE.md` and `.claude/settings*.json` in folders that aren't repos: those are stations set up by hand.
- **Repos still on `CLAUDE.md`:** repos under each root that have a `CLAUDE.md` and no `AGENTS.md`. Report them for the user to rename; leave them as they are.
- **Login hazards:** `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_PROFILE` exported in the environment or an rc file (any of them overrides every station's login), and a `~/.config/anthropic/` folder (a Console sign-in without an API key lives there, outside every config folder, so stations can't keep those apart).

Done when every config folder, every top-level folder under `$HOME`, and every skill, plugin and MCP server has been recorded.

## 3. Stations

- **Existing:** propose a station for each config folder and each folder set up by hand, marked *found, not made by /stations*.
- **Scratch:** ask which stations the user wants, suggesting `work`, `personal`, `research`. For each: name, root folder, one-line purpose.

Either way, settle which station is the default (it keeps `~/.claude` and its login). The others get `~/.claude-<name>`. Done when the user confirms the list.

## 4. Plan

One table, one row per surveyed item: item, kind, from, to, action, reason. Sort by matching each item's description against each station's purpose. When it's unclear, give it to every station and say so in the reason. Actions:

| Item | Rule |
|---|---|
| Loose skill, agent, rule | **move** to the one station that owns it. Needed in several: it stays in its owner's folder and the others get a **create** of a symlink to it. |
| Plugin | install it in each station that needs it (`CLAUDE_CONFIG_DIR=<dir> claude plugin marketplace add ...` then `plugin install`), and set it to `false` in `enabledPlugins` where it isn't needed. Plugin skills are never moved or linked: the plugin's repo stays their only source. |
| User MCP server | re-add it with `CLAUDE_CONFIG_DIR=<dir> claude mcp add --scope user ...` in each station that needs it; remove it from the default station when only other stations need it. Each add or remove is an **edit** of the file holding the server. |
| `settings.json` | a new station gets a copy of the default's, with its own `enabledPlugins`. Every station has `pluginConfigs."cc-plugin-agents-md@builtin".options.instructionFiles` set to `"claude-md-and-agents-md"`, so a repo's own `CLAUDE.md` doesn't hide the `AGENTS.md` files above it. |
| `<config>/CLAUDE.md` | its content moves to `~/AGENTS.md` (shared core) or `<root>/AGENTS.md` (one station only). A user-level `CLAUDE.md` loads in a single station, so it can't hold the shared core. |
| `<root>/AGENTS.md` | create it when missing: a heading and the station's purpose. |
| `projects/<key>/` | **move** to the station whose root contains the project path, so its history and auto memory follow it. |
| Shell | **create** `~/.config/claude-stations.sh` from `station-switch.sh` with the station map filled in, and **edit** `~/.zshrc` / `~/.bashrc` to source it. |

Show the table, then the hazards and the `CLAUDE.md` repos from step 2. The user edits rows until they confirm. Done when every surveyed item has a row and the user has confirmed the table.

## 5. Back up and apply

1. Create `~/.agent-config-backup-<YYYY-MM-DD-HHMM>/`. Copy `restore.sh` into it, plus a `README.md`: what the run did, and `bash restore.sh` to undo it.
2. Apply the rows in order. Write each action to `MANIFEST.tsv` **right after** it succeeds, so a run that fails halfway still restores. Before an **edit**, copy the file to `files/<absolute path>` inside the backup; that copy goes in the manifest row. To retire a file, **move** it into `files/` in the backup. Never delete anything.
3. Skip `projects/` content beyond the moves above: session history is large and moves undo cleanly.

Done when every confirmed row is applied and has its manifest line.

## 6. Check

Without calling the model, report for each station: its skills, agents, plugins, MCP servers, whether it has a login yet, and the `AGENTS.md` chain a sample repo under its root would load. Then:
- confirm where `CLAUDE_CONFIG_DIR=<new station> claude mcp add` wrote the server (`<dir>/.claude.json` or `~/.claude.json`), and fix the plan if it landed in the shared file;
- repeat the login hazards and the `CLAUDE.md` repos;
- on a re-check, also list: user-level items installed since the last run (they load in the default station everywhere outside a station root), items whose description doesn't match their station's purpose, and `settings.json` keys whose values differ between stations (report the drift, sync nothing);
- tell the user to open a new terminal tab, `cd` into a repo under each new station, run `claude`, `/login` once, and confirm the account in `/status`.

Finish with the backup folder's path and its restore command.
