---
name: execute-plan
description: Implement a scoped task or a plan phase in small verified steps with isolation, scope discipline and verification. Use on "execute the plan", "implement phase N", "ทำตามแผน", "build this" when the work spans several changes.
---

# Execute a scoped task
Finish the authorized scope; stop only at a real blocker.

1. Scope. Source is a plan phase (read `overview.md` and the phase file), a todo, or the user's request. Write down what changes and what does not.
2. Decompose into changes of one function/type plus its tests, or one bug fix. A single change needs no decomposition.
3. Isolate. For significant or concurrent work use `worktree-isolation`; small single-agent edits may stay in place. Back up persistent files before editing (owner rule).
4. Implement in order. Delegate only independent changes on different files to subagents (Sonnet for implementation, Haiku for mechanical edits); phases that feed each other run in sequence. Never let two workers edit one file.
5. Verify each change before the next: run the tests or the real command, and inspect the output. Use `verification-before-completion`. Do not continue past a failing check.
6. Commit only when the user asked for commits. Conventional style: `<type>(<scope>): <description>`, one logical change per commit.
7. Scope discipline: no speculative features, shims or defensive code. Report out-of-scope discoveries; do not fix them. If the plan is wrong or incomplete, say so instead of silently deviating.
8. Report in at most three lines: what changed, verified result, blocker.
