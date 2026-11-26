---
name: adversarial-review
description: Adversarial review of a finished change, plan or design by independent Claude reviewers with distinct lenses (Skeptic, Architect, Minimalist), ending in one verdict. Use on "adversarial review", "challenge this", "red-team this", "รีวิวแบบหาจุดอ่อน".
---

# Adversarial review
Deliverable is a verdict. Do not edit the reviewed work.

1. Identify the target (diff, plan, files) from the request or `git diff`. State its **intent** in one sentence: what the author wants. Reviewers judge whether the work achieves the intent, not whether the intent is right.
2. Size it and choose lenses (definitions in [lenses](references/lenses.md)). Take the larger of the line class and the file class. For a plan or design count the lines of the text under review. No target or an empty diff: ask what to review and stop.

| Size | Threshold | Reviewers (model) |
|---|---|---|
| Small | under 50 lines, 1-2 files | Skeptic (Sonnet) |
| Medium | 50-200 lines, 3-5 files | Skeptic (Opus) + Architect (Sonnet) |
| Large | 200+ lines or 5+ files | Skeptic (Opus) + Architect (Sonnet) + Minimalist (Sonnet) |

3. Spawn the reviewers in parallel, read-only, one message. Use the Agent tool with `model` set per row (`opus`, `sonnet`) and the prompt in [reviewer-prompt](references/reviewer-prompt.md). Give each the intent, its lens, the principles in [principles](references/principles.md), the owner rules that matter to this target (copy the few relevant lines from `shared-agent-rules.md` or `memory/preferences/user.md`; reviewers do not read private memory themselves) and the diff or file paths. If a model is unavailable or over quota, run that lens on `sonnet` and say so in the verdict. Distinct models are the point: do not run every reviewer on your own model. Opus is only for the Skeptic on medium/large work because of quota.
   - No Agent tool: write each prompt to a file under `mktemp -d`, then run `claude -p --model opus --allowedTools "Read,Grep,Glob" < "<dir>/skeptic.prompt" > "<dir>/skeptic.out" &` (read-only; use `sonnet` for the others), one background job per lens, then `wait`.
4. Confirm every reviewer returned text. If one failed or is empty, say so in the verdict; never skip silently.
5. Merge duplicates, apply the **Lead Judgment** (accept or reject each finding with one line; reviewers are adversarial by design, so reject style-as-substance and overreach), then compute the verdict from the accepted findings using [verdict-format](references/verdict-format.md).
6. Hand back the verdict. Apply fixes only if the user asks.
