# Lens: bugs

Find what the change makes wrong at runtime.

Look for:
- **Correctness:** logic errors, wrong conditions, off-by-one, wrong variable, inverted checks, state that is read before it is set.
- **Edge cases:** empty, null/None, zero, negative, very large, duplicate, unicode, concurrent calls, retries, partial failure.
- **Error handling:** exceptions swallowed or re-raised without context, missing cleanup, errors that turn into silent wrong results, data loss on a failed write.
- **Security** (sub-check): input reaching a query, shell, path, template or redirect without validation; a permission or ownership check missing on a new path; secrets in code or logs.
- **Performance** (sub-check): a query or network call inside a loop, an unbounded read, a missing timeout on an outbound call, work that grows with data size where it didn't before.
- **Tests** (sub-check): new branches or error paths with no test, tests that assert nothing meaningful, a test changed to match a bug.

Prove each finding: name the input or state that triggers it and what goes wrong. "Could be an issue if..." without a trigger is not a finding.

Leave to other lenses: style and naming (nitpicks), whether it matches house patterns (patterns), callers outside the diff (blast radius).
