# Lens: flow

Trace the execution and data path through the change, end to end.

Start at each entry point that reaches the changed code (an endpoint, a job, a CLI command, an event handler, a public function) and follow it through the change to where its effects land: database writes, network calls, queues, caches, files, emitted events, returned values.

Look for:
- Side effects the change adds, moves or removes that the function name or signature doesn't suggest.
- Ordering problems: a write before a validation, an event sent before the commit, a cache filled before the data is final.
- Transaction and retry boundaries: work that can now run twice, or half-run, when something fails partway.
- Data that changes shape along the path (types, units, nullability, encoding) without the next step expecting it.
- A path that no longer reaches code it used to reach, or now reaches code it shouldn't.

If a blame brief is in the prompt, use it to tell an intended path from an accident.

Prove each finding with the path: the hops as `file:line` in order, and the step where it goes wrong.

Leave to other lenses: single-line correctness (bugs), callers that the change doesn't run through (blast radius).
