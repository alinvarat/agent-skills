---
name: founder-consumer
description: Run independent simulated-buyer panels, validate answers and tally objections/prices; never claim measured customer conversion.
argument-hint: "[--n 100 | --quick] [--seed S]"
---

# Simulated buyer panel

**Check delegation first.** Without a sub-agent tool, prepare only the customer/pitch and requested number of briefs; report blocked and stop. Do not run `check`/`tally` or claim panel results. Steps 5–6 require actual independent answers.

1. Create `founder/customer.json` using [customer shape](customer.example.json): business, target, 2–4 segments with shares/income ranges, behaviors with shares, objections and optional habits. Prefer real interviews/reviews; label guesses. Show the short profile for correction before dealing.
2. Write one factual `founder/pitch.md` (product, price, delivery/availability). All buyers receive the identical pitch. Keep real prices unless the user adopts a change;
3. Sample: default 100. Translate the skill argument `--quick` to the helper option `init ... --n 20`; `panel.py` does not accept a `--quick` option; honor explicit `--n` and `--seed`. Tell the user the number of model calls before a large run. Always run `panel.py` from the project root — invoking it from inside `founder/` without `--dir panel` causes the default `founder/panel` target to create a nested `founder/founder/panel/` directory. Example for a quick run:
```bash
# Run from project root:
python3 "~/.claude/skills/founder-consumer/panel.py" init --customer founder/customer.json --pitch founder/pitch.md --n 20
python3 "~/.claude/skills/founder-consumer/panel.py" prompts
```
For another run, preserve the old directory and use a fresh `--dir PATH` **before every subcommand**. Never reuse old answers; `init` refuses populated runs.
4. For delegation only, read your agent runtime's delegation guidance. Run one independent agent per generated brief, bounded by available slots. Give only its brief and answer path; do not alter individual briefs. The moderator never writes buyer answers. Without delegation, prepare briefs and report blocked; do not fabricate a completed panel.
5. Run the same script with `check`. Retry only missing/broken answers once using `prompts`; then run `tally`. For an agent’s JSON reply, use `save ID` with that exact reply on stdin. Keep invalid/missing answers excluded and counted.
6. Read `founder/panel/results.md` and `.json`: report answered/missing counts, buy/pass and rate, differing segments, top objections with quotes, and what could change a no.

Done: tally matches validated answers and chosen run. These are simulations, not actual conversion, statistical bounds or customer testimonials. Validate major decisions with real buyers. Do not auto-run pricing or change a public offer.
