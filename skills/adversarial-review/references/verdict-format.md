# Verdict format
```
## Intent
<what the author wants>

## Verdict: PASS | CONTESTED | REJECT
<one-line summary>

## Findings (high -> low)
1. [severity] Description with file:line
   - Lens / model: who raised it
   - Principle: which one it breaks
   - Recommendation: concrete action

## What went well
<1-3 items no reviewer could fault>

## Lead judgment
<each finding: accept or reject, one line why>
```
Compute the verdict after Lead Judgment, from accepted findings only.
- PASS: no accepted high finding.
- REJECT: an accepted high finding that two reviewers raised, or that the only reviewer raised and you confirmed in the code.
- CONTESTED: an accepted high finding that only one of several reviewers raised, or reviewers disagree.
- A failed or empty reviewer is listed in the verdict; do not return PASS if the failed lens was the Skeptic.
