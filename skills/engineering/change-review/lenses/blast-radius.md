# Lens: blast radius

Find everything outside the diff that the change affects, and sibling code that still has the problem the change fixes.

For every changed symbol (function, method, class, constant, config key, schema, endpoint, event, CLI flag), search the repo for its users: `rg` for the name, plus imports, string references, serializers, fixtures and docs. If a blame brief is in the prompt, use it to find where the code came from.

Look for:
- **Broken callers:** a caller that relied on the old signature, return value, error, default, ordering or side effect.
- **Narrow patches:** the change fixes a problem in one place while the same pattern sits elsewhere (another caller of the same client without the timeout, another endpoint without the same check). List each sibling.
- **Contracts beyond the repo:** a public API, event payload, DB column, file format or config key that something outside this repo may read. Say it's outside and can't be checked from here.
- **Tests and fixtures** that pin the old behavior and will now fail or, worse, still pass for the wrong reason.

Prove each finding with the list: every caller or sibling as `file:line`, and the search you ran. A count without locations isn't checkable.

Leave to other lenses: bugs inside the diff itself (bugs), the end-to-end path through the change (flow).
