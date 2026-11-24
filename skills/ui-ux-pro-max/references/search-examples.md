## Example Workflow

**User request:** "Make an AI search homepage." (stack detected as Next.js from `package.json`)

```bash
# Step 2: design system
python3 "~/.claude/skills/ui-ux-pro-max/scripts/search.py" "AI search tool modern minimal" --design-system -p "AI Search"

# Step 3: supplement
python3 "~/.claude/skills/ui-ux-pro-max/scripts/search.py" "keyboard focus modal" --domain ux

# Step 4: stack guidelines
python3 "~/.claude/skills/ui-ux-pro-max/scripts/search.py" "suspense streaming bundle" --stack nextjs
```

Then synthesize the design system + detailed searches and implement.

## Output Formats

`--design-system` supports `-f ascii` (default, terminal display), `-f markdown` (documentation), and `--json` (machine-readable, includes the raw design system dict plus persistence status).

## Tips for Better Results

- Keep one dominant intent and 2–5 meaningful terms per query: `"keyboard focus modal"`, not a full audit checklist
- Retry once with a narrower phrase or explicit domain/stack; do not cycle through unrelated keywords
- Use `--design-system` for a new project/page and `--domain` for a focused concern
- Pass the detected stack explicitly for implementation-specific guidance

| Problem | What to Do |
|---------|------------|
| Can't decide on style/color | Re-run `--design-system` with different keywords |
| Dark mode contrast issues | `references/quick-reference.md` §6: `color-dark-mode` + `color-accessible-pairs` |
| Animations feel unnatural | `references/quick-reference.md` §7: `spring-physics` + `easing` + `exit-faster-than-enter` |
| Form UX is poor | `references/quick-reference.md` §8: `inline-validation` + `error-clarity` + `focus-management` |
| Navigation feels confusing | `references/quick-reference.md` §9: `nav-hierarchy` + `bottom-nav-limit` + `back-behavior` |
| Layout breaks on small screens | `references/quick-reference.md` §5: `mobile-first` + `breakpoint-consistency` |
| Performance / jank | `references/quick-reference.md` §3: `virtualize-lists` + `main-thread-budget` + `debounce-throttle` |
