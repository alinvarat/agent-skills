---
name: jlcpcb-parts-matcher
description: "Match KiCad BOM parts to live JLCPCB/LCSC stock, packages and ratings; apply verified LCSC fields when requested."
---

# Match JLCPCB assembly parts

1. Inspect the BOM: references, values, footprints, LCSC fields and build quantity. Group identical value + footprint. Before editing fields, back up the project. Audit/proposal requests produce a table; an existing request to apply fields needs no second approval.
2. Check live `jlcpcb.com/parts` / `lcsc.com` pages for exact part number, package/pitch, thermal pad, pin 1, ratings, class, quantity stock and unit price. Record date/source. Fees, stock and Basic/Preferred/Extended classes change; verify current fees before quoting savings. Missing evidence means **unverified**, not available.
3. Prefer compatible Basic/Preferred parts and reuse exact parts to reduce unique lines. For passives, check tolerance, dielectric and working-voltage/DC-bias derating (2× capacitor voltage is only a starting check). For diodes/MOSFETs/LDOs/ICs/connectors, use datasheets for pinout and relevant current, voltage, Rds(on), dropout and thermal limits.
4. Apply only verified exact matches within the authorized scope. A substitution changing electrical behavior, package or an unresolved constraint needs a user decision. Add `LCSC` fields, exclude DNP, and use `pcb-fab-prep` for BOM/CPL export. Inspect polarized-part/IC rotations in the assembly viewer.

Output in English: refs | original value/package | LCSC # | class | dated stock | quantity price | source/risk. Count unique Extended lines before/after and list missing evidence/footprint changes. Matching does not order parts; ordering requires a request and payment requires confirmation.
