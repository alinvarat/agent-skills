---
name: brainstorming
description: Find out what the user actually wants and why before building something new or ambiguous: look first, ask one question at a time, lay out approaches, write a short design and get approval. Use on new features, new tools, design questions, "ช่วยคิดก่อน", "brainstorm". Not for clear small tasks.
---

# Brainstorming
Goal: build what the user wants, not what you assume. The owner prefers few questions, so ask only what changes the outcome.

1. **What do you know?** Request fully specified and small (for example "make the icon blue"): do it and say what you did; this skill ends here. Something that changes the result is missing: continue.
2. **Look before asking.** Read the files, memory records, specs and code the user pointed at or the project holds (`memory` skill for history). Never ask what they already answer.
3. **First message (about 200 words).** Restate the request in your words (what, for whom, why as far as stated) and what you found that bears on it, including any constraint, conflict or cheaper path they may not have seen. Then one question: the biggest open point. Until you know *why* they want it, ask it open, in their terms, with no multiple choice. When the choices can be named, sketch each with its trade-off and your pick. If nothing is open, end with the short design and ask for approval. Unless they asked for brainstorming, add one line offering to just start.
4. **Conversation.** One question at a time, built on their last answer, in plain Thai at their level. State your call and reason as a proposal they can correct instead of asking about process or small choices. Cover: purpose and success, goals, non-goals, what would make it a failure, prior art, what exists now. Do recon (code, files, web) when it helps and say what you found. Play back each understood part in 200-300 words and ask what is wrong. Sketch layouts or flows as text when seeing helps.
5. **Approaches.** Once the want is clear, put the 2-3 real ways to build it in a message of its own, each with trade-offs and a recommendation; drop weak ones. If the user left the how to you, say you will use your pick. If there is one sensible way, say why the others fail.
6. **Size and design doc.** Say how big the work is (small change, or project). Write the design: intent and why, goals/non-goals/failure cases, constraints, approaches considered and the chosen one, decisions the user made (marked as theirs), your calls (marked as yours), what is left to the builder. Small change: a few lines. Project: full document, then have a fresh Sonnet subagent read it as the builder and list questions; settle answered and minor ones yourself and bring only the user-only questions in one message. Save under `<project>/docs/specs/YYYY-MM-DD-<topic>-design.md` (or a sensible place you name). Do not commit unless asked.
7. **Gate.** Build nothing (no product code, scaffolding, installs, new projects) until the user approves the design. Reading and exploring are fine. A spike the user agreed to may be built if labelled throwaway; keeping it is a new request through this gate. After approval, use `phased-plan`.

A design you have not written is not approved; "sounds good" to an idea covers only what you showed.
