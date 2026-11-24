"""Build a one-page Thai quotation or receipt (HTML + PDF) from a JSON spec.

Usage: python build_quote.py spec.json
Spec keys: see examples/esp32-board.json (quotation) and examples/receipt.json
(receipt, "doc": "receipt"). Output goes to spec["out_dir"] as
<Quotation|Receipt>_<job_slug>_<YYYY-MM-DD>.html/.pdf, with the logo copied next to the HTML.
Needs Google Chrome (headless) for the PDF; stdlib only otherwise.
"""
import argparse, base64, datetime, html, json, math, os, pathlib, re, shutil, subprocess, sys, tempfile

CHROME = [p for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser") if (p := shutil.which(name))] + [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    "/usr/bin/google-chrome",
]
ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")
MONTHS = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
          "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]

CSS = """
body{font-family:"PulseDoc","Tahoma",sans-serif;max-width:780px;margin:8px auto;padding:0 24px;color:#111;font-size:13.5px;line-height:1.5}
h1{font-size:26px;margin:0 0 4px}
.head{display:flex;justify-content:space-between;align-items:center}
.logo{width:90px;height:90px;border-radius:50%}
.meta{display:flex;justify-content:space-between;margin:16px 0;border-top:2px solid #111;border-bottom:1px solid #999;padding:10px 0}
table{width:100%;border-collapse:collapse;margin:12px 0}
th,td{border:1px solid #999;padding:8px 10px;text-align:left;vertical-align:top}
th{background:#eee}.r{text-align:right;white-space:nowrap}
h2{font-size:17px;margin:22px 0 4px}
ul{margin:4px 0 4px 20px;padding:0}
.c{text-align:center}
.sign{display:flex;justify-content:space-between;margin-top:40px;text-align:center}
.sign div{width:42%;padding-top:6px}
.sign div.role{width:auto;padding:0;margin:12px 0 8px}
.col{display:flex;flex-direction:column;gap:10px;width:330px}.col.rt{width:190px}
.row{display:flex;align-items:baseline;gap:2px}.row b{white-space:nowrap}.row .fill{flex:1;min-width:0}
.fill{display:inline-block;min-width:230px;border-bottom:1px dashed #111;padding:0 4px;line-height:1.1;vertical-align:baseline}
.fill:empty::before{content:'\\00a0'}
.fill.t{text-align:center}.fill.sm{min-width:36px}.fill.y{min-width:64px}.fill.p{min-width:80px}
@page{size:A4;margin:12mm}@media print{body{margin:0}}
"""


def font_css():
    """Embed the approved font in the HTML so every machine prints the same look."""
    css = ""
    for weight, name in ((400, "Regular"), (700, "Bold")):
        with open(os.path.join(ASSETS, "fonts", f"Sarabun-{name}.ttf"), "rb") as f:
            data = base64.b64encode(f.read()).decode()
        css += f'@font-face{{font-family:"PulseDoc";font-weight:{weight};src:url(data:font/ttf;base64,{data})}}'
    return css


def fill(text="", cls=""):
    return f'<span class="fill {cls}">{html.escape(text)}</span>'


def date_parts(iso):
    value = datetime.date.fromisoformat(iso)
    return value.day, value.month, value.year + 543


def validate_spec(spec):
    date_parts(spec["date"])
    items = spec.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("items must be a nonempty list")
    receipt = spec.get("doc") == "receipt"
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("desc"), str):
            raise ValueError("each item needs a text description")
        for key in (("qty", "price") if receipt else ("amount",)):
            value = item.get(key)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0 or (key == "qty" and value == 0):
                raise ValueError(key + " must be finite and nonnegative; quantities must be positive")
    total = sum(item["qty"] * item["price"] if receipt else item["amount"] for item in items)
    if not math.isfinite(total):
        raise ValueError("total exceeds the supported numeric range")


def build(spec):
    validate_spec(spec)
    d, m, y = date_parts(spec["date"])
    seller = spec.get("seller_name", "")
    receipt = spec.get("doc") == "receipt"
    total = sum(i["qty"] * i["price"] if receipt else i["amount"] for i in spec["items"])
    rows = "" if receipt else "".join(
        f'<tr><td>{n}</td><td>{html.escape(i["desc"])}</td><td class="r">{i["amount"]:,.2f}</td></tr>'
        for n, i in enumerate(spec["items"], 1))
    sections = "".join(
        f'<h2>{html.escape(s["title"])}</h2><ul>' + "".join(f"<li>{html.escape(x)}</li>" for x in s["items"]) + "</ul>"
        for s in spec.get("sections", []))
    fills = "".join(f"<li>{html.escape(f)}: {fill()}</li>" for f in spec.get("fill_in_terms", []))
    terms = spec.get("terms", [])
    cond = ""
    if terms or fills:
        cond = "<h2>เงื่อนไข</h2><ul>" + "".join(f"<li>{html.escape(t)}</li>" for t in terms) + fills + "</ul>"
    sdate = f'วันที่ {fill(str(d), "sm t")} / {fill(str(m), "sm t")} / {fill(str(y), "y t")}'

    def sign(name, role):
        return f'<div>( {fill(name, "t")} )<div class="role">{role}</div>{sdate}</div>'

    def meta_row(label, value, cls=""):
        return f'<div class="row"><b>{label}:</b>{fill(value, cls)}</div>'

    thai_date = f"{d} {MONTHS[m-1]} {y}"
    customer = spec.get("customer", "")
    if receipt:
        doc, sub, left, right, role = "ใบเสร็จรับเงิน", spec.get("title", "PULSE"), ("ได้รับเงินจาก", "ผู้รับเงิน"), meta_row("เลขที่", spec.get("number", ""), "t"), "ผู้รับเงิน"
        rows = "".join(
            f'<tr><td class="c">{n}</td><td>{html.escape(i["desc"])}</td><td class="c">{i["qty"]} {html.escape(i["unit"])}</td>'
            f'<td class="r">{i["price"]:,.2f}</td><td class="r">{i["qty"] * i["price"]:,.2f}</td></tr>'
            for n, i in enumerate(spec["items"], 1))
        head = '<tr><th style="width:48px" class="c">ลำดับ</th><th>รายการ</th><th style="width:70px" class="c">จำนวน</th><th class="r">ราคาต่อหน่วย (บาท)</th><th class="r">จำนวนเงิน (บาท)</th></tr>'
        foot = f'<tr><th colspan="4" class="r">รวมทั้งสิ้น</th><th class="r">{total:,.2f}</th></tr>'
    else:
        doc, sub, left, right, role = "ใบเสนอราคา", spec["title"], ("เสนอ", "ผู้เสนอ"), meta_row("ยืนราคา", f'{spec["validity_days"]} วัน' if spec.get("validity_days") is not None else "", "t"), "ผู้เสนอราคา"
        head = '<tr><th style="width:48px">ลำดับ</th><th>รายการ</th><th class="r">จำนวนเงิน (บาท)</th></tr>'
        foot = f'<tr><th></th><th class="r">รวมทั้งสิ้น</th><th class="r">{total:,.2f}</th></tr>'

    logo = '<img src="PULSE_logo.jpg" alt="logo" class="logo">' if spec.get("logo", True) else ""
    return f"""<!doctype html>
<html lang="th"><head><meta charset="utf-8"><title>{doc} {html.escape(sub)}</title><style>{font_css()}{CSS}</style></head><body>
<div class="head"><div><h1>{doc}</h1><div>{html.escape(sub)}</div></div>{logo}</div>
<div class="meta">
<div class="col">{meta_row(left[0], customer)}{meta_row(left[1], seller)}</div>
<div class="col rt">{meta_row("วันที่", thai_date, "t")}{right}</div>
</div>
<table>
{head}
{rows}
{foot}
</table>
{sections}{cond}
<div class="sign">{sign(seller, role)}{sign(customer, "ผู้ซื้อ")}</div>
</body></html>"""


def main(path):
    spec = json.load(open(path, encoding="utf-8"))
    validate_spec(spec)
    out = os.path.expanduser(spec["out_dir"])
    if not re.fullmatch(r"[A-Za-z0-9_-]+", spec.get("job_slug", "")):
        raise ValueError("job_slug must contain only English letters, digits, hyphens or underscores")
    os.makedirs(out, exist_ok=True)
    kind = "Receipt" if spec.get("doc") == "receipt" else "Quotation"
    base = f'{kind}_{spec["job_slug"]}_{spec["date"]}'
    hp, pp = os.path.join(out, base + ".html"), os.path.join(out, base + ".pdf")
    open(hp, "w", encoding="utf-8").write(build(spec))
    shutil.copy(os.path.join(ASSETS, "PULSE_logo.jpg"), os.path.join(out, "PULSE_logo.jpg"))
    chrome = next((c for c in CHROME if os.path.isfile(c)), None)
    if not chrome:
        sys.exit("Chrome not found; open the HTML and print to PDF")
    with tempfile.TemporaryDirectory() as profile:  # never attach to the user's running Chrome
        subprocess.run([chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--user-data-dir={profile}",
                        f"--print-to-pdf={pp}", pathlib.Path(hp).resolve().as_uri()],
                       check=True, capture_output=True, timeout=45)
    try:
        import pymupdf
        with pymupdf.open(pp) as pdf:
            pages = len(pdf)
    except ImportError:
        pages = len(re.findall(rb"/Type\s*/Page[^s]", pathlib.Path(pp).read_bytes()))
    print(hp, pp, f"pages={pages}", sep="\n")
    if pages != 1:
        raise ValueError(f"expected one page; generated {pages}. Revise the spec/layout before delivery.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build a one-page PULSE quotation or receipt")
    parser.add_argument("spec", help="JSON specification path")
    args = parser.parse_args()
    try:
        main(args.spec)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        parser.exit(1, str(exc) + "\n")
