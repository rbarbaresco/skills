# Lens: history

Find out why the touched code is shaped the way it is, and whether the change undoes a past decision.

The prompt carries a blame brief: for each changed block, the commit that last touched the surrounding lines and, where one was read, its PR. Start there. Go deeper only where a block looks deliberate or odd (a guard, a retry, a sleep, a special case, a magic number, a comment saying "don't"): `git log -L <start>,<end>:<file>`, `git log -S '<string>'`, `gh pr view <n> --comments`, and any ticket the PR links.

Look for:
- The change removes or weakens something that was added on purpose: a fix for an incident, a guard from a review thread, a workaround for a known upstream bug.
- The change reintroduces code that was removed before, and the removal said why.
- The change contradicts what a past PR or review agreed (a format, a limit, an ordering).
- The change repeats an approach a past PR tried and reverted.

Prove each finding with the past decision: the SHA and PR number, and a short quote of the reason from the PR or commit. If you can't find the origin, say "undocumented, couldn't find the origin" for that block under "Looked for, not found". Never write a rationale you didn't read.

Leave to other lenses: whether the change is correct on its own terms (bugs), who else calls it (blast radius).
