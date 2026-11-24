## 2. Upload & Name in Google Drive (when requested)
- Root `Document` URI (replace the placeholders with your own Drive account and folder IDs): `google-drive://<account>/<drive_id>/<document_folder_id>`
  - `Image` subfolder (`.png`): `<image_folder_id>`
  - `PDF` subfolder (`.pdf`): `<pdf_folder_id>`
- Upload each file directly into its matching subfolder, then rename it to a concise descriptive name matching the document title (e.g., `หนังสือให้ความยินยอม.png`, `หนังสือให้ความยินยอม.pdf`):
  ```bash
  BASE="google-drive://<account>/<drive_id>/<document_folder_id>"
  IMG_DIR="$BASE/<image_folder_id>"
  PDF_DIR="$BASE/<pdf_folder_id>"
  gio copy "$HOME/Pictures/<file>-rot.png" "$IMG_DIR/"
  gio copy "$HOME/Pictures/<file>-rot.pdf" "$PDF_DIR/"
  ```
- Note: `gio list` shows Drive file IDs by default. Find the newly copied ID with `gio list -d -l "$IMG_DIR"` / `"$PDF_DIR"`, then rename with `gio rename "<DIR>/<ID>" "<DocumentName>.png"` and verify display names and byte sizes with `gio list -d -l`.
- When archiving a PDF-only document (no scan PNG yet), keep `PDF` and `Image` subfolders in 1:1 parity (same count and matching base names):
  - Single-page PDF: render with `pdftoppm -png -r 300 -singlefile "<src.pdf>" "<out_prefix>"`.
  - Multi-page PDF: render all pages (e.g., `pymupdf` at 200+ dpi) and stitch them vertically with `PIL` into one `.png` — `-singlefile` only exports page 1 and silently drops the rest.
  - After uploading or when auditing completeness, verify live that both `Image` (`<image_folder_id>`) and `PDF` (`<pdf_folder_id>`) have equal file counts and matching names rather than relying on prior notes (via `gio list -d -l` or `google-workspace`'s `google_api.py drive search "'<FOLDER_ID>' in parents and trashed=false" --raw-query --max 50`, passing `--max` high enough that default pagination does not truncate the count).

- For a requested replacement, update the verified file ID in place if supported. Otherwise upload the new file, verify size and contents, then move the identified old copy to Trash. Check the final folder for duplicates and matching names.
