---
name: pcb-fab-prep
description: "Audit a finished KiCad board and export verified Gerber, drill and requested BOM/CPL files before fabrication."
---

# Prepare PCB production files

1. Identify the final revision, generated-source workflow and manual changes. Back up the project; do not regenerate away manual edits. Confirm service, layers, thickness/copper/finish and whether assembly is requested. Check current service capabilities.
2. Check installed `kicad-cli` options or use GUI checks. Refill zones; run latest ERC/DRC with all violations and unconnected items. Fix or justify each; do not silence findings to reach zero. Compare actual rules/stackup with service limits.
3. Inspect one closed outer Edge.Cuts boundary plus intentional closed inner cutouts: no gaps, overlaps or accidental islands. Check holes/slots, enclosure height/clearance, footprint-to-datasheet match, pin 1/polarity and readable silk off pads. For high-current nets, state copper/current/thermal assumptions; component ratings do not establish board ratings.
4. Export to a new `fab/<revision-date>/`: copper, mask, silk, outline and PTH/NPTH drills; paste and BOM/CPL only for requested assembly. Match service units/origin/rotation and exclude DNP. Zip the Gerber set; keep earlier exports.
5. Open the **exported** Gerbers in a viewer: layer order, side, outline, drills, mask and silk. Spot-check polarized/IC CPL rotations against the assembly/3D view.

6. JLC-class service: upload the zip to the service's DFM check before ordering and clear red/orange items. Observed analyser thresholds (JLC, 2026-10-13, provisional; recheck live): annular ring warns <0.15 mm; pad-to-edge warns <0.2 mm measured from the outline stroke; mask opening to trace warns <0.15 mm; THT-to-SMD flagged red <2.03 mm and orange <3.05 mm (plated mounting holes count as THT). Baseline floors used: copper clearance 0.17, trace >=0.15, via >=0.6/0.3, pad spacing >=0.2, copper-to-edge >=0.2-0.25 mm.
7. Assembly orders: API/library stock is not order-page proof. After upload, read the matched-parts table for Qty 0/unselected/warning rows and confirm assembly quantity equals the planned board count; move failing parts to hand-soldering or substitute. Check CPL origin equals the Gerber/drill origin, and include delivered-soldered parts such as sockets and headers. Downloaded datasheets must start with `%PDF` before text extraction.

Done: report revision, checks/results, open items, assumptions and file paths. Use `ready`, `ready with listed risks` or `not ready`; unresolved material connectivity, part, thermal or manufacturing issues mean **not ready**. Exporting is not ordering; orders need a request and payment needs confirmation. Project checkpoints stay in the project; memory writes follow `memory` triggers.
