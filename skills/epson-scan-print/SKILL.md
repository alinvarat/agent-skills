---
name: epson-scan-print
description: Scan documents to PNG/PDF, print single-sided or manual-duplex jobs on the local Epson L3256 (ET-2810) on Debian, and upload or rename scans in Google Drive.
---

# Epson L3256 (ET-2810) Scan & Print on Debian

**Print-request rule:** for "print trip/booking documents", print the original source documents (Trip.com/airline/hotel confirmation emails rendered to PDF, or voucher PDFs), not summaries or edited plans. Read emails via Gmail API payload parts (text/html) because `gmail get` can return an empty body. If the target is ambiguous (e.g. "แผน"), ask first or print the source docs.

## Scan Document
1. Detect the USB scanner dynamically:
   ```bash
   DEV=$(scanimage -L | sed -n "s/^device \`\(epsonds:[^']*\)'.*/\1/p" | head -n 1)
   ```
   If `$DEV` is empty, report that the Epson scanner is not detected (check power/USB) and stop.
2. Scan at 300 dpi Color into `~/Pictures/`:
   ```bash
   OUT="$HOME/Pictures/scan-$(date +%Y%m%d-%H%M%S).png"
   scanimage -d "$DEV" --format=png --resolution 300 --mode Color -o "$OUT"
   ```
3. Inspect `$OUT` visually (open the PNG with the host's image-reading tool, e.g. Claude Code `Read`, Hermes `read_file`) to check orientation, cropping, and legibility.
4. To correct orientation, choose `90`, `180` or `270` degrees counterclockwise after inspecting the scan. Pass the angle as the second argument and preserve the original file:
   ```bash
   python3 - "$OUT" 180 <<'PYTHON'
   import sys
   from pathlib import Path
   from PIL import Image
   source = Path(sys.argv[1])
   angle = int(sys.argv[2])
   with Image.open(source) as image:
       rotated = image.rotate(angle, expand=True)
       rotated.save(source.with_name(f"{source.stem}-rot.png"))
       rotated.convert("RGB").save(
           source.with_name(f"{source.stem}-rot.pdf"), resolution=300
       )
   PYTHON
   ```
   Re-inspect `*-rot.png` visually and check `pdfinfo "*-rot.pdf"` (page count, expected physical size from the scan dimensions at 300 dpi, non-zero file size) before reporting done.

### Photo-to-Scan A4 Cleanup (when given a phone photo)
1. Trim dark outer borders, normalize the white point (lift 95th-percentile RGB toward ~246), and apply mild contrast (~1.12) and sharpness (~1.35) boosts.
2. For ID/card photos, apply a rounded-corner mask onto a pure white background to remove corner shadows, scale to **actual ID-1 physical size** (`85.6 mm` wide -> `1011 px` at 300 dpi: `int(round(85.6 / 25.4 * 300))`), and **center both horizontally and vertically** on a 300 dpi A4 canvas (`2480 x 3508` px: `pos_x = (2480 - w) // 2`, `pos_y = (3508 - h) // 2`).
3. Export `<name>.png`, `<name>.pdf` (color), and `<name>-ขาวดำ.pdf` (grayscale) before archiving or printing.
4. When printing an actual-size A4 PDF (such as an ID card), omit `-o fit-to-page` (use `lp -d EPSON_L3256 -o Ink=MONO -o media=A4 "FILE.pdf"`) so CUPS preserves true physical dimensions. For a requested Drive replacement, follow the archival workflow below.

## Archive in Drive
Read [Drive archival and naming](references/drive-archive.md) when the user requests Drive upload, replacement or an archive audit.

## Print Document
1. Check CUPS queue status:
   ```bash
   lpstat -p -d
   ```
   Default queue is `EPSON_L3256` (`printer-driver-escpr`). If the queue is disabled or unplugged, report and stop.
2. Check PDF page count and paper size first: `pdfinfo "FILE.pdf"`.
3. **Single-sided**:
   ```bash
   lp -d EPSON_L3256 "FILE.pdf"
   ```
   - Black & white / Grayscale (ขาวดำ): pass `-o Ink=MONO` (default driver option is `COLOR`).
   - Paper sizing: pass `-o media=A4 -o fit-to-page` to scale margins cleanly.
   - Multi-image inputs: combine document images into a single A4 PDF with Pillow (`save_all=True, append_images=..., resolution=300.0`) and print the PDF rather than queuing separate raw image jobs.
4. For two-sided printing, follow [manual duplex](references/manual-duplex.md).

5. Verify queue completion with `lpstat -o EPSON_L3256` (empty when finished), `lpstat -p EPSON_L3256`, and `lpstat -W completed -o EPSON_L3256 | tail -n 5`. Do not rely on `lpq` (`cups-bsd` is not installed by default on minimal Debian).
