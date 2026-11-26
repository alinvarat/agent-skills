---
name: reflect
description: Review the current conversation for mistakes, corrections, user preferences, gotchas and repeated manual steps, then propose where each lesson belongs (memory, a skill, a script or check). Use only on the user's request: "reflect", "สรุปบทเรียน", "ถอดบทเรียน".
---

# Reflect
Never run on your own. The user's request to reflect authorizes proposing and saving lessons through the `memory` skill's rules; completion of a task alone does not.

1. Read `<memory-root>/index.md`, then `rg` the keywords of each candidate lesson in `memory/indexes/` and `memory/preferences/`, so you do not re-record known facts. A missing file is reported, not invented.
2. Scan this conversation for: mistakes and the user's corrections (quote their words), stated preferences and workflow habits, verified gotchas of tools or systems, decisions with their reason, friction with skills or delegation, and manual steps repeated more than twice.
3. Drop trivia and anything already recorded or derivable from code or git.
4. Route each lesson. Check first whether it can be enforced structurally (a script, hook, lint, config flag); if yes, propose that instead of a note.
   - User preference or correction: `memory/preferences/user.md` or the matching topic file; if it fits none or several, use `user.md` and link the topic. Dated, with a one-line why.
   - Facts about a task or system: invoke the `memory` skill with the accepted rows; the user's request to reflect is the explicit save request it requires.
   - How a specific skill should behave: edit that skill's SKILL.md or reference only for a row the user accepted (read it first; avoid contradicting it). After a skill edit, apply the owner's standing rule: sync sanitized public copies (no private paths, IDs or personal data) to the `agent-skills` monorepo and the `skill-<name>` repo. Report each push.
   - Follow-up work: say it in the summary; add it to Google Tasks only if asked.
5. Show the proposed entries in a short table (lesson, evidence, destination). Apply those the user accepts. "Save" or "จำเลย" means apply all memory rows only; skill edits still need an accepted row. Before editing a preference file copy it to `memory/archive/<name>.bak-<timestamp>`; if the copy fails, stop. Never store secrets or tokens.
6. Verify by reading back each file and index row you touched. Summary in at most three lines.
