---
name: freecad-part-design
description: "Create or edit FreeCAD parts with an editable Part Design feature tree; preserve existing geometry and appearance."
---

# FreeCAD Part Design

1. Read the user's hardware preferences if they provide them. Find the user's target or current GUI/MRU; default project folder `~/Project/FreeCad`. Inspect tree, dependencies, dimensions, local edits and open-document state.
2. **Back up before editing.** Record object names, visibility/appearance and archive entries: `GuiDocument.xml`, `ShapeAppearance*`, `LineColorArray*`, `PointColorArray*`, thumbnails. Coordinate GUI and disk copies so a later GUI save cannot discard newer work.
3. Model separate physical parts as separate Bodies with sketches and native Pad/Pocket/Hole/Revolve/Fillet/Pattern features. Preserve design intent and constrain sketches where practical. Do not replace the tree with one opaque `Part::Feature`, primitive/boolean-only solid or mesh. Explain a Part Design limitation before changing approach.
4. Recompute; check broken features, shape validity, solid count and dimensions. Save editable `.FCStd`, preferably from the GUI. Reopen it and inspect useful views/tree. Headless recompute alone does not verify appearance.
5. Compare saved GUI/archive entries **and actual ViewObject Visibility/ShapeAppearance** with the backup. Preserve hidden alternates and unrelated choices; no unexplained differences. A visible Body with hidden Tip can render blank.

Before using a visibility helper, or if headless saving removes GUI data, read [appearance recovery](references/appearance-recovery.md). Preserve current geometry; never restore backup `Document.xml` over it. Old face arrays require compatible identities/topology; otherwise restore appearance in the GUI.

## Headless pitfalls (FreeCAD 1.1)
- `FreeCADCmd -c "code"` fails (args are treated as file paths): write a script file and run `FreeCADCmd script.py`. Offscreen GUI: `timeout 180 xvfb-run -a FreeCAD macro.FCMacro`, wrap in `try/except` with `finally: sys.exit(0)`; a failing macro otherwise hangs. Judge success from files written (PNG, log), not exit code (GUI exits 1; the `amdgpu.ids` message is harmless). Kill only your own FreeCAD.
- FreeCADCmd has no `FreeCADGui`; `pivy.coin` can fail: use `ActiveView.viewAxonometric()/fitAll()`. Screenshot without touching the camera to test that visibility persisted.
- A FreeCADCmd save drops `GuiDocument.xml`: check `unzip -l f.FCStd | grep GuiDocument.xml`. Save files with materials/appearance from the same offscreen GUI macro (`sk.touch(); body.touch(); doc.recompute(); doc.save()`); never swap `Document.xml` between zips (stale `.brp` reverts geometry).
- Pad/Pocket direction: use `SideType` ('One side'/'Two sides'/'Symmetric'), not deprecated `Midplane`.
- Before editing, check for user changes since last session (timestamp, `.FCBak`, `body.Tip`); chain new features onto their latest Tip, never an older feature. "Add" means a new body/object, not replace. Keep experiments under a temp name until verified.
- Diagnose before declaring a defect: separate real geometry faults from display artifacts (overlaid axis, stale shape). Involute gear collar tangent to the root can create OCCT tessellation slivers: step the collar down ~50 µm.
- Overwriting a wrapper symlink (e.g. FreeCAD -> AppRun) with `tee`/redirect destroys the target: `rm -f` the link first.

Done: report saved path, tested geometry/dimensions and actual appearance comparison. If GUI/appearance checks are unavailable, state that limitation first. Print preparation uses `3d-print-prep`.
