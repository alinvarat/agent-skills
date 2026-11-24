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
| [`caveman`](skills/caveman) | Use only on an explicit caveman-mode request. Short grammatical replies; normal mode or stop caveman ends it. | [repo](https://github.com/alinvarat/skill-caveman) |
| [`copywriting`](skills/copywriting) | Write or edit marketing copy, headlines and CTAs. Preserve supplied facts and voice; keep point edits within scope. | [repo](https://github.com/alinvarat/skill-copywriting) |
| [`debian-desktop-control`](skills/debian-desktop-control) | Capture screenshots or control the local Debian GNOME Wayland desktop. Use for explicit screen, mouse or keyboard requests. | [repo](https://github.com/alinvarat/skill-debian-desktop-control) |
| [`design-critique`](skills/design-critique) | Get structured design feedback on usability, hierarchy and consistency from a Figma link, screenshot or mockup, at any stage from exploration to final polish. | [repo](https://github.com/alinvarat/skill-design-critique) |
| [`document-suite`](skills/document-suite) | Create, convert or audit local Thai/English documents and PDFs. Use Sarabun for Thai text. | [repo](https://github.com/alinvarat/skill-document-suite) |
| [`ee-datasheet-master`](skills/ee-datasheet-master) | Extract verified chip values, pinouts, addresses, timing or registers from the actual manufacturer datasheet/PDF. | [repo](https://github.com/alinvarat/skill-ee-datasheet-master) |
| [`epson-scan-print`](skills/epson-scan-print) | Scan documents to PNG/PDF, print single-sided or manual-duplex jobs on the local Epson L3256 (ET-2810) on Debian, and upload or rename scans in Google Drive. | [repo](https://github.com/alinvarat/skill-epson-scan-print) |
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
| [`google-calendar`](skills/google-calendar) | Read or change Google Calendar events, availability and recurring schedules; sync a compatible widget when requested. | [repo](https://github.com/alinvarat/skill-google-calendar) |
| [`google-tasks`](skills/google-tasks) | Read, add, complete or delete Google Tasks. Verify the list/task target and read back changes. | [repo](https://github.com/alinvarat/skill-google-tasks) |
| [`grill-me`](skills/grill-me) | Compatibility alias for explicit grill-me requests; load the grilling interview workflow. | [repo](https://github.com/alinvarat/skill-grill-me) |
| [`grilling`](skills/grilling) | Stress-test a user plan through focused decision questions. Use when an interview or grill is requested. | [repo](https://github.com/alinvarat/skill-grilling) |
| [`hallmark`](skills/hallmark) | Design new websites, landing pages and web UI screens that look designed, not generated. Use when asked to build or design a new page/site, or when Hallmark is named; never on an existing design unless named. | [repo](https://github.com/alinvarat/skill-hallmark) |
| [`jlcpcb-parts-matcher`](skills/jlcpcb-parts-matcher) | Match KiCad BOM parts to live JLCPCB/LCSC stock, packages and ratings; apply verified LCSC fields when requested. | [repo](https://github.com/alinvarat/skill-jlcpcb-parts-matcher) |
| [`kicad-board-design`](skills/kicad-board-design) | Design, edit or review KiCad schematics and PCB layouts with engineering calculations, SI/PI, EMC, thermal, mechanical and manufacturing checks. | [repo](https://github.com/alinvarat/skill-kicad-board-design) |
| [`linux-troubleshooting`](skills/linux-troubleshooting) | Diagnose Linux incidents in CPU, memory, disk, services, networking, databases, TLS, backups or deployments. | [repo](https://github.com/alinvarat/skill-linux-troubleshooting) |
| [`maker-showcase-site`](skills/maker-showcase-site) | Build or fix the user's personal/PULSE showcase website (alinvarat.github.io) or GitHub profile, including 3D robots and boards made from the user's real FreeCAD, KiCad or EasyEDA files. Use for bio/link pages, portfolio pages, 3D product scenes and publishing work to GitHub. | [repo](https://github.com/alinvarat/skill-maker-showcase-site) |
| [`pcb-fab-prep`](skills/pcb-fab-prep) | Audit a finished KiCad board and export verified Gerber, drill and requested BOM/CPL files before fabrication. | [repo](https://github.com/alinvarat/skill-pcb-fab-prep) |
| [`ponytail`](skills/ponytail) | Simplify a coding solution without losing required behavior. Use for ponytail, YAGNI or over-engineering requests. | [repo](https://github.com/alinvarat/skill-ponytail) |
| [`product-marketing`](skills/product-marketing) | Create or update reusable product marketing context: positioning, audience, voice, proof and tested learnings. | [repo](https://github.com/alinvarat/skill-product-marketing) |
| [`product-photo-poster`](skills/product-photo-poster) | Build a PULSE product-photo poster with Thai text and logo. Square 1:1 by default; no video or carousel. | [repo](https://github.com/alinvarat/skill-product-photo-poster) |
| [`psp-media-manager`](skills/psp-media-manager) | On Windows, copy owned PSP games/homebrew and back up saves on a verified PSP USB drive; eject safely. | [repo](https://github.com/alinvarat/skill-psp-media-manager) |
| [`pulse-team`](skills/pulse-team) | Coordinate the PULSE Hermes/Discord bot team (Chief, IT, Developer, Engineer and other department bots): route work, @mention bots, follow up and post status safely. | [repo](https://github.com/alinvarat/skill-pulse-team) |
| [`quotation-maker`](skills/quotation-maker) | Create the PULSE one-page Thai quotation or receipt as HTML/PDF with Sarabun, logo and signature blocks. | [repo](https://github.com/alinvarat/skill-quotation-maker) |
| [`restart-handoff`](skills/restart-handoff) | Hand off to a new chat on เริ่มใหม่; save context, launch Claude and verify receipt. Not for restarting devices/apps/tasks. | [repo](https://github.com/alinvarat/skill-restart-handoff) |
| [`sales-enablement`](skills/sales-enablement) | Create sales decks, one-pagers, objection responses, demos, proposals or ROI models from supported product facts. | [repo](https://github.com/alinvarat/skill-sales-enablement) |
| [`systematic-debugging`](skills/systematic-debugging) | Diagnose bugs and failed tests from evidence; reproduce, test one cause, apply a bounded fix and verify the original symptom. | [repo](https://github.com/alinvarat/skill-systematic-debugging) |
| [`ui-ux-pro-max`](skills/ui-ux-pro-max) | Search local UI design systems, accessibility guidelines, patterns and stack-specific implementation advice for web, mobile and desktop. | [repo](https://github.com/alinvarat/skill-ui-ux-pro-max) |
| [`ux-copy`](skills/ux-copy) | Write or review UX copy — microcopy, error messages, empty states, CTAs, confirmation dialogs and onboarding text. | [repo](https://github.com/alinvarat/skill-ux-copy) |
| [`verification-before-completion`](skills/verification-before-completion) | Check actual changed behavior and outputs before claiming complete, fixed or passing; disclose what remains unverified. | [repo](https://github.com/alinvarat/skill-verification-before-completion) |
| [`windows-health-check`](skills/windows-health-check) | Measure Windows temperature, load, drivers or power settings. Use linux-troubleshooting for Linux incidents. | [repo](https://github.com/alinvarat/skill-windows-health-check) |
| [`writing-for-agents`](skills/writing-for-agents) | Write or revise skills and AGENTS.md/CLAUDE.md instructions with clear triggers, executable steps and scoped reference loading. | [repo](https://github.com/alinvarat/skill-writing-for-agents) |
| [`zero-to-pass-tutor`](skills/zero-to-pass-tutor) | Tutor a zero-foundation learner for an exam or technical topic using worked examples first, single-step pacing, single-twist difficulty scaling, problem-recognition drills, active review quizzes, and terminal-safe math. | [repo](https://github.com/alinvarat/skill-zero-to-pass-tutor) |

## Third-party sources

Some skills are adapted from open-source projects; each keeps its upstream license and names its source in its own `README.md`: caveman (Apache-2.0), copywriting, product-marketing and sales-enablement (MIT), design-critique and ux-copy (Apache-2.0), hallmark (MIT), ponytail (MIT), ui-ux-pro-max (MIT).

Author: Linwrath_Pulse
