# Approved quotation/receipt spec and layout

Read before preparing the spec; keep this template unless the user requests changes.

- Font Sarabun (bundled and embedded), one A4 page. Logo `assets/PULSE_logo.jpg` top-right; Thai document title left, job title below.
- Blank fields use aligned dashed lines directly after labels, including the seller name. Do not invent customer identity.
- Seller: the seller name from the spec (examples use the fictional "นายตัวอย่าง นามสมมติ"). Date is today in Asia/Bangkok; PDF uses Buddhist year.
- Identical signature structures: `( name )`, role, `วันที่ d / m / y`. Quote seller role ผู้เสนอราคา; receipt role ผู้รับเงิน; customer role ผู้ซื้อ. Keep lines, roles and dates separated.
- Keep the blank กำหนดส่งงาน field. Do not add exclusions, customer-deliverables or payment terms unless requested. Validity/revision counts/other terms require actual agreement; missing fields stay blank.
- Receipt: do not add "ได้รับเงินถูกต้องแล้ว". Use `doc: "receipt"`, `number` blank if absent, `customer`, items with `desc`, `qty`, `unit`, `price`; total is computed. Example: `examples/receipt.json`.
- Quote: `out_dir`, `job_slug`, `title`, `date` (YYYY-MM-DD), `items` (`desc`, `amount`), `sections`, `terms`, `fill_in_terms`; example `examples/esp32-board.json`.
- Price hints are examples only (use supplied prices; no assistant-chosen discounts): 1,000 THB per item is a typical placeholder.
- Output names: `Quotation_JOB_DATE` or `Receipt_JOB_DATE`, HTML+PDF with copied logo. `out_dir` is required (for example `~/Quotes`); job slug uses English letters/digits/hyphens/underscores.
