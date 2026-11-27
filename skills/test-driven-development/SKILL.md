---
name: test-driven-development
description: Write the failing test first, watch it fail for the right reason, then write minimal code. Use before implementing any feature, bug fix, refactor or behavior change in code that has or can have tests. "ทำแบบ TDD", "เขียนเทสก่อน".
---

# Test-driven development
Iron law: no production code without a failing test first. Code written before its test is deleted and redone from the test; do not keep it as "reference".

Exceptions (ask the user first): throwaway prototypes, generated code, configuration. If the project forbids local runs, still write the test first and verify through that project's CI instead of running it here.

## Cycle
1. **Red.** Write one test for one behavior, with a name that states the behavior, using real code (mocks only when unavoidable). Before writing it, name the production change whose absence would make it fail.
2. **Verify red (mandatory).** Run it. It must fail (not error) with the expected message because the feature is missing. Passes immediately: you test existing behavior, fix the test. Errors: fix until it fails correctly.
3. **Green.** Write the simplest code that passes. No extra options, no refactoring beyond the test.
4. **Verify green (mandatory).** The new test passes, and the project's whole suite passes (bare `pytest`, `npm test`, `cargo test`, whatever the repo uses), output without warnings. Any failure the run shows, even one you did not cause, is named in your report. A scope statement bounds the deliverable, not the verification.
5. **Refactor** only while green: remove duplication, improve names, no new behavior. Repeat with the next failing test.

## Test rules
- One behavior per test; "and" in the name means split it.
- Assert real behavior, never that a mock was called.
- Keep test-only code in test utilities, not in production classes.
- Understand a dependency's side effects before mocking it. Must mock everything: the code is too coupled; inject dependencies. Huge setup: simplify the design.
- Bug fix: first a failing test that reproduces the bug; never fix a bug without one.

## Excuses that mean start over
"too simple to test"; "I'll test after" (a test written after passes at once and proves nothing); "already tested manually" (no record, not repeatable); "deleting hours of work is wasteful" (sunk cost); "keep it as reference"; "TDD is dogmatic here"; "this case is different". Hard to test means hard to use: change the design.

## Done checklist
Every new function has a test; each test was seen failing for the right reason; code is minimal; whole suite is green; edge cases and error paths are covered. A box that cannot be ticked means the cycle was skipped: redo it.
