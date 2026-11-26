# Reviewer lenses
Each reviewer takes exactly one lens.

## Skeptic (correctness and completeness)
- Which inputs, states or sequences break this?
- Which error paths are unhandled or swallowed?
- Which races or ordering dependencies exist?
- What does the author assume that is not proven? Where does "works on my machine" stand in for verification?
Principles: prove-it-works, fix-root-causes.

## Architect (structural fitness)
- Does the design serve the stated goal or an assumed one?
- Where are the coupling points that hurt when requirements shift?
- Where does responsibility leak between components?
- Which assumption about scale, concurrency or ordering breaks first?
Principles: boundary-discipline, redesign-from-first-principles.

## Minimalist (necessity)
- What can be deleted without losing the goal?
- Which problems is the author solving before having them?
- Which abstraction has one call site? Which option has no second use?
- Is this the simplest path, or the one that felt most thorough?
Principles: subtract-before-you-add, outcome-oriented-execution.
