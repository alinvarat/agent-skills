---
name: verification-before-completion
description: Check actual changed behavior and outputs before claiming complete, fixed or passing; disclose what remains unverified.
---

# Verify before delivery
1. Define the observable result required by the user.
2. Run the relevant check on current state. Read the actual result and exit code; recheck after further relevant edits.
3. Inspect the output: reproduce the bug, reopen the file, view the rendered artifact, or read back external state. Another agent’s summary, file existence or exit code alone is insufficient.
4. Reconcile all requested items with checked/blocked items. Report what changed, the supported result and material gaps. If verification is unavailable, say so first; do not imply success.

Use checks that prove behavior, not wording-matching tests. Check visual quality, hardware and live-account effects separately; metadata parsing cannot prove them. After a timeout, inspect external state before retrying. Once required checks pass, deliver; broaden/repeat checks only for a change, failure or unresolved concern.
