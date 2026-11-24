---
name: quotation-maker
description: Create the PULSE one-page Thai quotation or receipt as HTML/PDF with Sarabun, logo and signature blocks.
---

# Quotation / receipt

1. Read the user's saved business preferences, if available, then [spec/layout](references/spec-layout.md). Use the supplied price/deliverables; never add a discount. Unknown customer/terms stay blank. Ask only for required price/deliverables that are still missing.
2. Copy the quote or receipt example named in that reference. Set required `out_dir`, safe `job_slug`, today's Asia/Bangkok date and agreed items. Retain Sarabun, PULSE logo, dashed fields and paired signatures. Do not add unagreed commercial terms or payment declarations.
3. Run:
   `python3 "~/.claude/skills/quotation-maker/scripts/build_quote.py" spec.json`
   Edit JSON and rebuild for revisions; do not patch generated HTML. Back up an existing deliverable before replacing it.
4. Require exit success and `pages=1`. Render/open the PDF; check Thai marks, totals, no clipping and aligned signature blocks. Check Sarabun embedding. Rendered appearance matters even when extracted Thai looks garbled.
5. Return the PDF using the host's attachment/link capability. Do not send it to a customer without an explicit instruction. Save notes or tick a task only on explicit request.

Missing browser/assets, invalid numbers or a multi-page result are blockers to delivery; report the issue and fix the spec rather than label an unchecked quote complete.
