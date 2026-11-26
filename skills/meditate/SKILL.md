---
name: meditate
description: Audit the shared memory records, preferences and installed skills for stale, duplicated, low-value or bloated content and skill descriptions, then propose and apply approved cuts. Use on "meditate", "audit memory", "clean up skills", "ตรวจความจำและสกิล".
---

# Meditate (memory and skill audit)
Targets: `<memory-root>/` (index, indexes, preferences, tasks), the Claude auto-memory at `<claude-auto-memory>/`, `<home>/.claude/CLAUDE.md`, and `<skills-root>/*/SKILL.md`. Do not touch the gdrive-sync system.

Quality bar: an entry earns its place only if it is high-signal (the model would otherwise get it wrong), high-frequency, or high-impact. Everything else is noise.

1. Snapshot. Build one text file per target group under the scratch directory with `for f in <files>; do echo "=== $f ==="; cat "$f"; done > "<scratch>/snapshot-<group>.md"`. Large trees: list sizes first with `du -a` and snapshot only index, preferences, and the 30 most recently changed task files.
2. Audit with a Sonnet subagent per group (memory; skills) in parallel, read-only, prompt in [agents](references/agents.md). Skip a group with under 3 expected findings by checking it yourself.
3. Verify every "stale" claim against current state before accepting it (does the file, tool, service or decision still exist? `ls`, `rg`, `systemctl`).
4. Present one report: per item the path, the flag (outdated, redundant, low-value, verbose, orphaned, contradicts another record, bloated description), evidence and the proposed action (update, merge, condense, delete).
5. Apply only what the user approves. Back up each file first to `memory/archive/<name>.bak-<timestamp>`; stop if the copy fails. Merge into the stronger record and delete the weaker. Memory deletion is permanent: list the exact records and get a yes first.
6. Skill changes follow `writing-for-agents`. After editing shared skills apply the owner's standing rule: sync sanitized public copies (no private paths, IDs or personal data) to `agent-skills` and `skill-<name>`, and report each push.
7. Re-read changed files, confirm index rows still link to existing files, report counts: deleted, condensed, merged, skill descriptions tightened.
