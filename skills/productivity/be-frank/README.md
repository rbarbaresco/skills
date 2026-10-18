# be-frank

Get an honest, researched answer to "does this already exist, and is it worth building?" before you spend months on an idea.

**Type:** user-invoked. Run `/rbarbaresco-skills:be-frank` yourself; Claude never starts it on its own.

## Usage

```
/rbarbaresco-skills:be-frank a CLI that turns OpenAPI specs into typed TypeScript clients with zero runtime deps, built-in retry and Zod validation, against openapi-typescript, orval and hey-api
```

Claude needs three things, and asks for whichever is missing:

- **What:** the idea: a description, a spec, a file or a link.
- **Against:** what to compare it with: named products, a category, or a market. Claude never assumes "the whole market". It can suggest a few sets, but you pick.
- **Goal:** a tool for yourself, a product for strangers, an open-source project, a business. The verdict depends on it, so Claude always asks for it, offering 2 to 4 goals that fit your idea.

If the idea is too vague to compare ("an AI productivity app"), Claude says so and asks specific questions instead of guessing what you meant.

## What you get

- **Verdict:** a few frank sentences, split by goal when that changes the answer.
- **Feature table:** each of your features checked against each alternative (✅ full, ◐ partial, ✗ not found), with a source link for each mark.
- **Similarity %:** per alternative and combined, counted from the table: full = 1, partial = 0.5, divided by the number of features.
- **Differences that matter:** what nobody else does, what everyone has but you don't, where alternatives are stronger.
- **Risks:** how high the leading alternative sets the bar, adoption, monetization and licence limits, scope.
- **What to focus on,** the decisions left to you, and dated sources.

## How it works

1. **Intake:** agree the what, the against and the goal, and which connected tools Claude may use besides web search.
2. **Vagueness check:** turn the idea into a list of checkable features, and confirm it with you.
3. **Research:** confirm the list of alternatives, then check every feature against primary sources (docs, pricing pages, repos, store listings).
4. **Report** in chat.

## Limitations

- **Needs web search.** Subagents make it faster but are optional.
- **"Not found" isn't "doesn't exist".** The research is a sample; the report says so.
- **Facts are dated.** Features and prices change, so recheck before a big decision.
- **The report isn't saved.** Copy it from the chat if you want to keep it.

## Files

| File | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | The instructions Claude follows for intake, the vagueness check, research and the report |
