# Lens: nitpicks

Small things that make the change harder to read or maintain. All findings here are `consider`.

Look for:
- Names that mislead or don't match how the repo names the same thing.
- Dead code, leftover debug output, commented-out blocks, unused imports or parameters.
- Comments that restate the code, or are now wrong after the change.
- Small duplication inside the diff that one local variable or helper would remove.
- Formatting the repo's own formatter or linter config would flag.

Check the repo's linter and formatter config before raising style: never suggest something the config contradicts, and skip anything the formatter would fix on its own if the repo runs it in CI.

Prove each finding with where the repo does it differently, or which config rule applies.

Leave to other lenses: anything that changes behavior (bugs, flow), house patterns beyond naming and style (patterns).
