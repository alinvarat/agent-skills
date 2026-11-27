---
name: requesting-code-review
description: Ask an independent reviewer subagent to review finished work against its requirements before moving on or merging. Use after each task of a larger plan, after a major feature, before merge, or when stuck. For a hostile multi-lens review use adversarial-review.
---

# Requesting a code review
Review early and often; the reviewer gets crafted context, never your session history.

1. Get the range: `BASE_SHA=$(git merge-base origin/main HEAD)` (or the commit before the task) and `HEAD_SHA=$(git rev-parse HEAD)`. For uncommitted work, use `git diff` text instead of SHAs.
2. Spawn one read-only `general-purpose` subagent on `sonnet` (Opus only for risky or security-sensitive changes) with the prompt in [reviewer-prompt](references/reviewer-prompt.md), filled with: what was built, the requirements or plan, BASE_SHA, HEAD_SHA.
3. Act on the result: fix Critical issues now, fix Important issues before continuing, note Minor ones. If the reviewer is wrong, push back with code or test evidence (see `receiving-code-review`).
4. Never skip review because the change is "simple", never proceed with unfixed Critical or Important issues, and do not review a large diff inline yourself: that spends the context you need to drive the work.
