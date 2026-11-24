# Appearance preservation and recovery

Read before using a visibility helper or repairing a headless save.

## Preserve visibility and appearance
- Show the requested finished parts; preserve intentionally hidden alternates and existing layer/object choices. A visible Body with a hidden Tip may render blank.
- If you have a visibility helper script (such as a `freecad_visibility.py`): call `apply_visibility` with explicit visible/hidden Body names and `hide_others=False` when existing unrelated display choices must remain; then inspect `assert_visibility` results. Its defaults show every Body and hide other objects, and it hides Origin objects even with `hide_others=False`; snapshot and restore unrelated view flags explicitly rather than applying it blindly to an existing document.
- Headless saves can omit GUI ZIP entries. Compare the saved archive against the backup before delivery. If entries disappear, prefer reopening in the GUI and restoring the baseline appearance there.
- If a headless-recovery route is necessary, rebuild the archive in the backup’s original entry order, combining current Document.xml/shape data with compatible GUI/appearance entries from the backup; simply appending missing files is insufficient. Preserve the current geometry, never replace Document.xml with the backup’s version.
- Before reusing old per-face appearance data, check that object identities and face mapping are still compatible. When topology changed, reapply the intended appearance in the GUI rather than attaching arrays to different faces. Compare ZIP entry names/counts and actual ViewObject Visibility/ShapeAppearance with the backup: no unexplained differences; list any user-requested display changes explicitly.

