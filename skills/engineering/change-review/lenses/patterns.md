# Lens: patterns

Check whether the change does things the way *this* repo already does them.

Sources of "the way this repo does it", in order of weight:
1. The repo's instruction files and docs (`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, ADRs, style guides) and what they import.
2. Code next to the change: the same module, sibling files, the same layer elsewhere.
3. Framework or library features the repo already uses for the same job.

Look for:
- Hand-written code where the repo already has a helper, wrapper, base class or component for it.
- A new pattern for something the repo does one consistent way elsewhere (error handling, logging, config access, HTTP clients, DB access, test fixtures).
- A rule from the repo's own docs that the change breaks.
- A framework feature that already solves what the change builds by hand.

Prove each finding with the existing example: the `file:line` that does it the house way, and how many places follow it (`rg` count). One other usage is a coincidence; a doc rule or several usages is a pattern. If the repo is inconsistent itself, say so instead of picking a side.

Leave to other lenses: runtime bugs (bugs), naming and formatting (nitpicks).
