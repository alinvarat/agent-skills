---
name: product-marketing
description: 'Create or update reusable product marketing context: positioning, audience, voice, proof and tested learnings.'
metadata:
  version: 2.2.0
---

# Product marketing context

1. Find existing project context: `.agents/product-marketing.md`; then `.claude/product-marketing.md` or legacy `product-marketing-context.md` in those folders. Keep the user-chosen location. Propose a migration before moving a legacy file.
2. Distinguish **read**, **create**, and **update**. Reading context for a copy task does not authorize file changes. If creation is requested, draft from the brief/relevant project evidence, or interview one useful section at a time. If updating, change only requested sections and preserve the rest.
3. Read [context schema](references/context-schema.md) for a new document or matching section; use [brand voice](references/brand-voice.md) for voice extraction. Keep exact customer words. Label decisions, measured results, estimates and unknowns; omit irrelevant sections, never invent proof.
4. Save an authorized change without an extra approval loop. New: `Document version: v1`, today's ISO date, one initial Changelog entry. Substantive update: increment version, update date, prepend one line naming changed sections/reason; preserve older entries. Typo-only corrections do not bump the version.
5. Read back changed sections, version/date and untouched content. Report saved path/revision. Do not promise every host auto-discovers it.

Learnings rows contain **learning / evidence with sample size / applies to / active|watch|retired**. Measured results and user decisions with reasons can qualify; a single anecdote is at most `watch`. Put objections/customer language in their own sections. Retire only with a stated reason such as contradictory evidence or changed product; age alone is insufficient. Preserve retired history; archive when over about 20 active rows. An unrequested learning may be proposed, not silently saved. No scheduled loop is authorized.
