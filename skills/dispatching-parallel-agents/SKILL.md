---
name: dispatching-parallel-agents
description: Split 2 or more independent problems (different failing test files, subsystems or bugs, no shared state) across parallel subagents with focused, self-contained prompts, then integrate and verify. Use on "run these in parallel", several unrelated failures. Not for related failures or exploratory debugging.
---

# Dispatching parallel agents
One agent per independent problem domain; agents never inherit your session, you write exactly what they need.

1. **Check independence.** Group failures by what is broken. Parallel only if fixing one cannot affect another, no shared files or resources, and each can be understood alone. Related failures, unknown root causes and shared state: investigate together or run sequentially.
2. **Write one prompt per agent**, self-contained: the specific scope (one file or subsystem), the goal, pasted error messages and test names, constraints ("do not change other code", "tests only"), what to do first (read, find the root cause, no blind timeout increases), and the exact output: root cause, files changed, anything unverified.
3. **Choose models** (quota rule): Haiku for mechanical edits, Sonnet for investigation and implementation, Opus only for the hardest judgement.
4. **Dispatch all agents in one message** so they run concurrently (one per message is sequential). Cap at about 3-4 at once.
5. **Integrate.** Read each summary, check that no two agents edited the same code, run the full suite, spot-check for systematic errors, and use `verification-before-completion` before reporting.
