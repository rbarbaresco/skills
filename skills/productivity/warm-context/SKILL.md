---
name: warm-context
description: Builds and loads warm-context packs, researched domain knowledge (concepts, options, trade-offs, pitfalls) stored as indexed Markdown so a planning session starts warm. Use when the user runs /warm-context <topic>, asks to warm up on or study a domain, or a task matches a pack listed in the warm-context catalog.
compatibility: Needs web search. Uses subagents or a deep-research skill when available.
---

# warm-context

A **pack** is a domain's knowledge, not steps for doing a task in it. For "bake a pie", a pack covers pastry science, pie families, fillings and their trade-offs, and common failures. It leaves out the recipe. Packs feed a later planning session.

**Library:** `.warm-context/` in the session's working directory, so a project carries its own context. Never use a `.warm-context/` from a parent folder, even if its catalog is in context. If `./.warm-context/` is missing, create it. The library holds `CATALOG.md` and one folder per pack, `<library>/<slug>/`.

The first time you write a pack into the library, wire it up:
1. Create `.warm-context/CATALOG.md` with a `# Warm-context packs` heading if it's missing.
2. Add this block to `AGENTS.md` in the working directory, creating the file if needed. Skip it if the file already mentions `.warm-context/CATALOG.md`.

   ```markdown
   ## Warm-context packs

   Researched domain knowledge for this project lives in `.warm-context/`. When a task touches a pack listed below, load it with the warm-context skill.

   @.warm-context/CATALOG.md
   ```
3. Claude Code skips `AGENTS.md` by default when the folder also has a `CLAUDE.md`. If there is a `CLAUDE.md` that doesn't import `AGENTS.md`, add the same block there too.
4. Tell the user where the library is, which instruction files you edited, and that they can commit or gitignore `.warm-context/`.

## 1. Match

Read `<library>/CATALOG.md` and match the topic against each pack's description, not only its slug ("pies" and "pastry" may be the pie pack).
- One clear match → **Load**.
- Several plausible matches, or a weak one → ask the user which pack, or whether to start a new one.
- No match → **Intake**.

## 2. Load

1. Read the pack's `INDEX.md` and `overview.md`. Open topic files only when the work touches them.
2. **Freshness:** if the Scope block says `fast-moving` and the research date is more than 6 months ago, tell the user and offer a refresh.
3. **Gap check:** compare the user's current task against the pack's Coverage block. Name any part of the task the pack doesn't cover (items under *Seen but not researched*, or anything absent) and offer a gap pass. A gap pass runs **Research** on just those subtopics, adds or extends files, moves items into *Covered*, and updates the date in `INDEX.md` and the catalog.

The pack is a partial sample of the domain, not its boundary. If something isn't in the pack, treat it as unresearched, not as nonexistent.

Load is done once the index and overview have been read and freshness and gaps have been reported, or reported as fine.

## 3. Intake

Ask 3–5 questions in a single message. The user can answer "just go", in which case you infer reasonable answers and state them.
- **Goal:** what will the user plan or do with this knowledge?
- **Constraints:** equipment, skill level, stack, budget: whatever narrows the domain.
- **Out of scope:** what to leave out on purpose.
- **Volatility:** `stable` (pie baking) or `fast-moving` (a JS framework). Propose one.
- **Sources beyond the web:** list the MCP tools or connectors in this session that look relevant, if any, and have the user confirm which may be used. Use none that weren't confirmed.

Plan up to 8 subtopics that cover what the goal needs: concepts, the option space, rules of thumb, failure modes.

## 4. Research

Use the first route that's available:
1. A skill for multi-source research with subagents (for example `deep-research`). Hand it the scope and subtopics.
2. Subagents. Send one per subtopic, each following [references/research-loop.md](references/research-loop.md).
3. Inline. Follow the same loop yourself, one subtopic at a time.

Every route's output gets rewritten in step 5. Research is done once every planned subtopic has sourced findings, or a note saying why it came up empty.

## 5. Write

Write the pack in the format set out in [references/pack-format.md](references/pack-format.md). Add or update its line in `CATALOG.md`, then **Load** it.
