# Agent Skills

A collection of reusable skills (instruction packages) for AI coding agents such as Claude Code. Each skill lives in `skills/<name>/` with a `SKILL.md` that tells the agent when to use it and what steps to follow.

## Install

Copy or symlink the skills you want into your agent's skills folder, for example:

```bash
git clone https://github.com/alinvarat/agent-skills.git
ln -s "$PWD/agent-skills/skills/systematic-debugging" ~/.claude/skills/
```

Some skills reference helper scripts; paths in examples assume the skill is installed under `~/.claude/skills/`.

## Skills

| Skill | What it does | Repo |
|---|---|---|
| [`3d-print-prep`](skills/3d-print-prep) | Check a finished CAD part for printing: valid solid, walls, fit, orientation, supports and verified export. | [repo](https://github.com/alinvarat/skill-3d-print-prep) |
| [`arduino-robotics-libraries`](skills/arduino-robotics-libraries) | Write or fix Arduino/robotics libraries, firmware and examples while preserving the target board, API and project style. | [repo](https://github.com/alinvarat/skill-arduino-robotics-libraries) |
| [`document-suite`](skills/document-suite) | Create, convert or audit local Thai/English documents and PDFs. Use Sarabun for Thai text. | [repo](https://github.com/alinvarat/skill-document-suite) |
| [`ee-datasheet-master`](skills/ee-datasheet-master) | Extract verified chip values, pinouts, addresses, timing or registers from the actual manufacturer datasheet/PDF. | [repo](https://github.com/alinvarat/skill-ee-datasheet-master) |
| [`ffmpeg-video-toolkit`](skills/ffmpeg-video-toolkit) | Edit or inspect video/audio with FFmpeg: size limits, loudness, vertical crop and audio extraction. | [repo](https://github.com/alinvarat/skill-ffmpeg-video-toolkit) |
| [`founder-board`](skills/founder-board) | Review a business idea through three framework lenses; produce a fund/pass vote, risks, conditions and evidence gaps. | [repo](https://github.com/alinvarat/skill-founder-board) |
| [`founder-brand`](skills/founder-brand) | Develop business names, voice and a visual identity brief. Use for naming or brand strategy, not automatic image generation. | [repo](https://github.com/alinvarat/skill-founder-brand) |
| [`founder-cfo`](skills/founder-cfo) | Calculate unit economics, break-even, cash needs and financial scenarios from sourced inputs; not a full business-plan compiler. | [repo](https://github.com/alinvarat/skill-founder-cfo) |
| [`founder-competitors`](skills/founder-competitors) | Research competitors, substitutes, comparable prices and customer complaints for a defined market; cite current public sources. | [repo](https://github.com/alinvarat/skill-founder-competitors) |
| [`founder-consumer`](skills/founder-consumer) | Run independent simulated-buyer panels, validate answers and tally objections/prices; never claim measured customer conversion. | [repo](https://github.com/alinvarat/skill-founder-consumer) |
| [`founder-launch`](skills/founder-launch) | Plan a dated business launch, demand test and launch-day run sheet; publishing, buyer contact and spending require their own request. | [repo](https://github.com/alinvarat/skill-founder-launch) |
| [`founder-marketing`](skills/founder-marketing) | Plan positioning, channels, budget and a dated campaign from customer evidence; use copywriting for a standalone copy edit. | [repo](https://github.com/alinvarat/skill-founder-marketing) |
| [`founder-offer`](skills/founder-offer) | Improve offer structure, deliverables and guarantees using buyer objections and costs; preserve baseline pitches and panel runs. | [repo](https://github.com/alinvarat/skill-founder-offer) |
| [`founder-ops`](skills/founder-ops) | Plan fulfilment, staffing, suppliers, SOPs, capacity and local compliance; separate sourced operating costs from assumptions. | [repo](https://github.com/alinvarat/skill-founder-ops) |
| [`founder-plan`](skills/founder-plan) | Compile existing Founder artifacts into a business plan and one-page brief with a calculated, qualified financial verdict. | [repo](https://github.com/alinvarat/skill-founder-plan) |
| [`founder-pricing`](skills/founder-pricing) | Analyze survey/panel price sensitivity, competitors and margins to propose price tests; do not change actual prices automatically. | [repo](https://github.com/alinvarat/skill-founder-pricing) |
| [`freecad-part-design`](skills/freecad-part-design) | Create or edit FreeCAD parts with an editable Part Design feature tree; preserve existing geometry and appearance. | [repo](https://github.com/alinvarat/skill-freecad-part-design) |
| [`grill-me`](skills/grill-me) | Compatibility alias for explicit grill-me requests; load the grilling interview workflow. | [repo](https://github.com/alinvarat/skill-grill-me) |
| [`grilling`](skills/grilling) | Stress-test a user plan through focused decision questions. Use when an interview or grill is requested. | [repo](https://github.com/alinvarat/skill-grilling) |
| [`jlcpcb-parts-matcher`](skills/jlcpcb-parts-matcher) | Match KiCad BOM parts to live JLCPCB/LCSC stock, packages and ratings; apply verified LCSC fields when requested. | [repo](https://github.com/alinvarat/skill-jlcpcb-parts-matcher) |
| [`kicad-board-design`](skills/kicad-board-design) | Design, edit or review KiCad schematics and PCB layouts with engineering calculations, SI/PI, EMC, thermal, mechanical and manufacturing checks. | [repo](https://github.com/alinvarat/skill-kicad-board-design) |
| [`linux-troubleshooting`](skills/linux-troubleshooting) | Diagnose Linux incidents in CPU, memory, disk, services, networking, databases, TLS, backups or deployments. | [repo](https://github.com/alinvarat/skill-linux-troubleshooting) |
| [`pcb-fab-prep`](skills/pcb-fab-prep) | Audit a finished KiCad board and export verified Gerber, drill and requested BOM/CPL files before fabrication. | [repo](https://github.com/alinvarat/skill-pcb-fab-prep) |
| [`systematic-debugging`](skills/systematic-debugging) | Diagnose bugs and failed tests from evidence; reproduce, test one cause, apply a bounded fix and verify the original symptom. | [repo](https://github.com/alinvarat/skill-systematic-debugging) |
| [`verification-before-completion`](skills/verification-before-completion) | Check actual changed behavior and outputs before claiming complete, fixed or passing; disclose what remains unverified. | [repo](https://github.com/alinvarat/skill-verification-before-completion) |
| [`windows-health-check`](skills/windows-health-check) | Measure Windows temperature, load, drivers or power settings. Use linux-troubleshooting for Linux incidents. | [repo](https://github.com/alinvarat/skill-windows-health-check) |
| [`writing-for-agents`](skills/writing-for-agents) | Write or revise skills and AGENTS.md/CLAUDE.md instructions with clear triggers, executable steps and scoped reference loading. | [repo](https://github.com/alinvarat/skill-writing-for-agents) |
| [`zero-to-pass-tutor`](skills/zero-to-pass-tutor) | Tutor a zero-foundation learner for an exam or technical topic using worked examples first, single-step pacing, single-twist difficulty scaling, problem-recognition drills, active review quizzes, and terminal-safe math. | [repo](https://github.com/alinvarat/skill-zero-to-pass-tutor) |

Author: Linwrath_Pulse
