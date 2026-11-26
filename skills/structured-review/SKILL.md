---
name: structured-review
description: Interactive review of a plan or code change through Architecture, Code Quality, Tests and Performance, with numbered issues and lettered options; also a post-work quality gate. Use on "review this", "check my changes", "ตรวจงานนี้", "quality gate". For a hostile multi-model challenge use adversarial-review instead.
---

# Structured review
Deliverable is the review. Make no changes.

1. Find the scope from the request, `git diff`, or the named plan/PR. Ask only if nothing can be inferred.
2. Size: BIG (50+ changed lines, 3+ files or new architecture) = all four sections, at most 4 issues each. SMALL = one issue per section.
3. Gather context. SMALL: read the files directly. BIG: use `Explore` subagents (Haiku or Sonnet) in parallel to read the code, callers, types and tests.
4. If a domain skill matches (for example `kicad-board-design`, `arduino-robotics-libraries`, `ui-ux-pro-max`), invoke it and apply its constraints.
5. Review, in order:
   - Architecture: boundaries, coupling, data flow, single points of failure, security boundaries.
   - Code quality: structure, duplication, error handling, missing edge cases, over- or under-engineering.
   - Tests: coverage gaps, assertion strength, untested failure paths.
   - Performance: repeated work, memory, slow paths, caching.
6. Number every issue. For each give: the concrete problem with file:line, 2-3 lettered options (include "do nothing" when sensible) with effort, risk and maintenance cost, and a recommended option with the reason. If something can be tested, say how.
7. Present all sections together, then ask once for direction. Do not assume timelines or scale.

## Post-work gate mode
Use when the user asks to check finished work or says "quality gate". Run in order and stop at the first high issue:
1. Scope: `git diff --stat`; flag files outside the agreed scope.
2. Verification: run the project's tests/lint that exist; invoke `verification-before-completion`.
3. Principles in [principles](references/principles.md).
4. Test evidence: new behavior has a test that asserts outcomes.
Report ACCEPT or REJECT with specific files and reasons. Do not ask the user mid-gate.
