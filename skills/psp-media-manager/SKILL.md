---
name: psp-media-manager
description: On Windows, copy owned PSP games/homebrew and back up saves on a verified PSP USB drive; eject safely.
---

# PSP media manager (Windows)

This workflow uses Windows drive letters. On Debian, report that limitation before writing; do not reinterpret a target automatically.

1. Check saved notes from earlier installs, if available, to avoid reinstalling known ARK-4 content. Identify the actual FAT32 PSP drive by label, capacity and `PSP` folder (usually `ISO`/`SEPLUGINS` too). Do not write if identity is uncertain; never format/empty without an explicit request.
2. Check free space with margin and the exact file limit: **4,294,967,295 bytes**. Compression may not fit. Split only if the specific loader supports the format. Use only the user's owned dumps or selected homebrew.
3. Copy to the right place: PSP `.iso/.cso` → `ISO\`; PS1/homebrew/PSN `EBOOT.PBP` → `PSP\GAME\APP\`; saves → `PSP\SAVEDATA\`. Keep filenames simple and folders shallow. Do not put raw PS1 ISO files in `ISO\`.
4. Preserve existing games/saves/plugins. Before an authorized replacement, make a timestamped backup. Save backups use the chosen path or `<project folder>\PSP-Backups\YYYYMMDD-HHmm\`. Do not edit ARK-4 or `SEPLUGINS` except the requested change; show before/after text. Cleanup: list sized candidates, then delete only selected items.
5. Verify copy sizes and SHA-256 hashes, list destination files/free space, and safely eject before unplugging. Report drive, copied files, backup path and gaps in Thai. Copy success does not prove it runs on the PSP.
