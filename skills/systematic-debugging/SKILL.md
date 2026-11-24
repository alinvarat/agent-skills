---
name: systematic-debugging
description: Diagnose bugs and failed tests from evidence; reproduce, test one cause, apply a bounded fix and verify the original symptom.
---

# Debug a failure
1. Read the actual error. Record expected/observed behavior, target and recent changes. Reproduce when permitted. If reproduction is unavailable, state what evidence is missing.
2. Trace the first bad input/output/configuration boundary. Compare a nearby working case. Choose one hypothesis and the cheapest check that distinguishes it. Do not print credentials or unrelated logs.
3. Before a consequential fix, keep a failing reproducer/regression check. A reversible wording change needs inspection, not a test of the wording. Preserve the before state/rollback for persistent edits.
4. Fix the cause once, including affected callers and error handling. Stay within the authorized scope; do not stack speculative fixes or add unrelated cleanup.
5. Repeat the original reproducer and relevant checks using `verification-before-completion`. Inspect actual behavior/artifacts, then deliver.

If a fix fails, return to step 2. After three failed hypotheses/fixes, reassess the architecture/environment and report the blocker plus the next discriminating check. Ask only for genuinely unavailable information/authority. A vanished intermittent symptom is not proof of a fix.

Read only when needed: [downstream error tracing](root-cause-tracing.md), [validation at multiple boundaries](defense-in-depth.md), [asynchronous waiting](condition-based-waiting.md).
