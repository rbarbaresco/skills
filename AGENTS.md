# Repo conventions

This repo is a Claude Code plugin (`rbarbaresco-skills`) and its own single-plugin marketplace (`rbarbaresco`).

- Skills live in bucket folders under `skills/`: `engineering/` (code and production work) and `productivity/` (everything else). One folder per skill, with its `SKILL.md`.
- Every shipped skill has an entry in `.claude-plugin/plugin.json`'s `skills` array **and** a linked entry in `README.md` under **User-invoked** or **Model-invoked**. Add or remove both together.
- User-invoked skills set `disable-model-invocation: true` in their frontmatter; model-invoked skills don't.
- Agents in `agents/` are namespaced by the plugin. Reference them as `rbarbaresco-skills:<agent-name>` (for example in a workflow script's `agentType`).
- Paths to files inside the plugin use `${CLAUDE_PLUGIN_ROOT}` in skill and agent Markdown. Never hardcode a home directory.
- Nothing personal or employer-specific: no names of internal services, companies, people, or local paths.
- After touching either manifest, run `claude plugin validate . --strict`.
- Users only receive a change when `version` in `.claude-plugin/plugin.json` is bumped. Bump it (semver) and add a `CHANGELOG.md` entry in the same PR as any user-visible change.
