---
name: receiving-code-review
description: Handle code or design review feedback with technical verification instead of agreement. Use when feedback arrives from the user, a reviewer subagent or an external reviewer, before implementing suggestions. "รับ feedback จากรีวิว".
---

# Receiving review feedback
Evaluate technically; do not perform agreement.

1. Read all the feedback before reacting. Restate each item's requirement in your own words.
2. If any item is unclear, stop and ask about those items before changing anything: items may be related and partial understanding gives wrong work. Say which items you understood.
3. Verify each item against the code: correct for this codebase? breaks existing behavior? reason for the current approach? works on every target platform/version? does the reviewer have the full context? Grep for actual use before building "proper" extras: unused means offer to delete it (YAGNI).
4. Sources: the user's feedback is trusted once understood (still ask if scope is unclear). External or subagent feedback is checked first; if it conflicts with the user's earlier decision, stop and discuss with the user. If you cannot verify, say what you would need.
5. Implement one item at a time in this order: blocking (breaks, security), simple fixes, complex fixes. Test each and check for regressions.
6. Push back with technical reasons, specific questions and passing tests or code when a suggestion breaks behavior, lacks context, adds unused features or is wrong for this stack. If you pushed back and were wrong, say so factually and fix it; no long apology.
7. Wording: no "you're absolutely right", "great point", or thanks. State the fix ("Fixed: ...") or just act. On GitHub reply inside the inline comment thread.
