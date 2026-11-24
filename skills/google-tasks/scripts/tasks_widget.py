"""Desktop widget: Google Tasks on the top-left of the desktop, frosted-glass card.

Run with pythonw (no console):  pythonw tasks_widget.py
Needs gtasks.py authorized (token in %LOCALAPPDATA%\\gtasks). Stdlib only (+ Windows PowerShell
for rendering the glass background from the wallpaper via render_card_bg.ps1).
- Click the circle to mark a task done. Right-click the card to refresh now.
- Sits below normal windows (HWND_BOTTOM). Background = blurred, tinted wallpaper behind it.
"""
import ctypes
import ctypes.wintypes
import datetime
import glob
import json
import os
import shutil
import subprocess
import sys
import threading
import time
import tkinter as tk
import tkinter.font as tkfont

try:  # crisp text: opt out of Windows bitmap scaling on scaled displays
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    pass
try:
    S = ctypes.windll.user32.GetDpiForSystem() / 96.0
except Exception:
    S = 1.0
K = 0.9      # overall widget size (1.0 = original). Scales geometry and fonts together.
S *= K


TALL_H = int(570 * S)     # Tasks and Calendar cards share this minimum height


def _fs(pt):
    return max(7, int(round(pt * K)))

HERE = os.path.dirname(os.path.abspath(__file__))
GTASKS = os.path.join(HERE, "gtasks.py")
RENDER = os.path.join(HERE, "render_card_bg.ps1")
SENSORS = os.path.join(HERE, "sensors.ps1")
CACHE = os.path.join(os.environ.get("LOCALAPPDATA", HERE), "gtasks", "cache")
PY = sys.executable
X, Y = int(28 * S), int(64 * S)            # top-left, just under the top bar
WIDTH = int(310 * S)
PAD = int(18 * S)
RADIUS = int(20 * S)
THICK = 1.6                                 # border width in px (physical)
REFRESH_MS = 3 * 60 * 1000
ALPHA = 0.78     # window translucency (1.0 = opaque); desktop shows through
KEY = "#010101"                         # transparent corners only
FG, DIM, ACCENT = "#f6f0ff", "#cbbfe3", "#b99bff"   # violet palette, matches the purple wallpaper
RED, AMBER, GREEN = "#ff8fb0", "#e3c8ff", "#b99bff"   # same hue family: hot / warm / base
LINE = "#8272a8"
TRACK = "#3a2f55"
FONT = "Leelawadee UI"
MAX_ROWS = 40
NOWIN = 0x08000000       # CREATE_NO_WINDOW


def run(*args):
    p = subprocess.run([PY, GTASKS, *args], capture_output=True, text=True,
                       encoding="utf-8", creationflags=NOWIN, timeout=60)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def fetch():
    code, out = run("list")
    if code != 0:
        return None, out.strip()
    rows = []
    for line in out.splitlines():
        if not line.startswith("["):
            continue
        _, _, rest = line.partition("] ")
        tid, due, title = (rest.split("\t") + ["", ""])[:3]
        rows.append((tid, due, title))
    rows.sort(key=lambda r: (r[1] == "", r[1]))   # dated first, soonest first
    return rows, ""


def due_badge(due):
    """(text, colour) for a YYYY-MM-DD due date."""
    if not due:
        return "", DIM
    try:
        d = datetime.date.fromisoformat(due)
    except ValueError:
        return due, DIM
    n = (d - datetime.date.today()).days
    label = d.strftime("%d %b")
    if n < 0:
        return "%s  late" % label, RED
    if n == 0:
        return "today", RED
    if n == 1:
        return "tomorrow", AMBER
    if n <= 3:
        return "%s  (%dd)" % (label, n), AMBER
    return label, DIM


class MemStatus(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]


def ram_usage():
    m = MemStatus()
    m.dwLength = ctypes.sizeof(MemStatus)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    total = m.ullTotalPhys
    used = total - m.ullAvailPhys
    return used / 1024 ** 3, total / 1024 ** 3


def disk_usage():
    d = shutil.disk_usage("C:\\")
    return (d.total - d.free) / 1024 ** 3, d.total / 1024 ** 3


def net_octets():
    """Total (in, out) octets over operational ethernet/wifi adapters (legacy GetIfTable, 32-bit counters)."""
    size = ctypes.c_ulong(0)
    ctypes.windll.iphlpapi.GetIfTable(None, ctypes.byref(size), False)
    buf = ctypes.create_string_buffer(size.value)
    if ctypes.windll.iphlpapi.GetIfTable(buf, ctypes.byref(size), False) != 0:
        return None
    n = int.from_bytes(buf.raw[0:4], "little")
    tin = tout = 0
    for i in range(n):
        o = 4 + i * 860
        typ = int.from_bytes(buf.raw[o + 516:o + 520], "little")
        oper = int.from_bytes(buf.raw[o + 544:o + 548], "little")
        if typ in (6, 71) and oper in (4, 5):
            tin += int.from_bytes(buf.raw[o + 552:o + 556], "little")
            tout += int.from_bytes(buf.raw[o + 576:o + 580], "little")
    return tin, tout


def fmt_speed(bps):
    if bps >= 1024 * 1024:
        return "%.1f MB/s" % (bps / 1048576.0)
    return "%d KB/s" % round(bps / 1024.0)


def level_colour(pct):
    return GREEN if pct < 60 else (AMBER if pct < 85 else RED)


def wallpaper_path():
    buf = ctypes.create_unicode_buffer(520)
    ctypes.windll.user32.SystemParametersInfoW(0x73, 520, buf, 0)  # SPI_GETDESKWALLPAPER
    return buf.value


def wrap(font, text, width):
    """Greedy wrap by words; falls back to characters for long words (Thai has no spaces)."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip() if cur else word
        if font.measure(trial) <= width:
            cur = trial
            continue
        if cur:
            lines.append(cur)
            cur = ""
        while font.measure(word) > width:
            n = len(word)
            while n > 1 and font.measure(word[:n]) > width:
                n -= 1
            lines.append(word[:n])
            word = word[n:]
        cur = word
    if cur:
        lines.append(cur)
    return lines or [""]


class Widget:
    def __init__(self):
        r = self.root = tk.Tk()
        r.overrideredirect(True)
        r.configure(bg=KEY)
        r.attributes("-transparentcolor", KEY)
        r.attributes("-alpha", ALPHA)
        r.geometry("%dx%d+%d+%d" % (WIDTH, 80, X, Y))
        self.canvas = tk.Canvas(r, bg=KEY, highlightthickness=0, bd=0, width=WIDTH, height=80)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-3>", lambda e: self.refresh_once())
        mb = self.mbox = tk.Toplevel(r)
        mb.overrideredirect(True)
        mb.configure(bg=KEY)
        mb.attributes("-transparentcolor", KEY)
        mb.attributes("-alpha", ALPHA)
        self.mcanvas = tk.Canvas(mb, bg=KEY, highlightthickness=0, bd=0, width=WIDTH, height=80)
        self.mcanvas.pack(fill="both", expand=True)
        self.mbg = None
        self.f_head = tkfont.Font(family=FONT, size=_fs(14), weight="bold")
        self.f_count = tkfont.Font(family=FONT, size=_fs(11))
        self.f_title = tkfont.Font(family=FONT, size=_fs(11), weight="bold")
        self.f_due = tkfont.Font(family=FONT, size=_fs(9), weight="bold")
        self.f_circle = tkfont.Font(family=FONT, size=_fs(13))
        self.bg_img = None
        self.wall = wallpaper_path()
        self.sens = {}
        self.f_cell = tkfont.Font(family=FONT, size=_fs(9), weight="bold")
        self.f_cellv = tkfont.Font(family=FONT, size=_fs(10), weight="bold")
        self.start_sensors()
        self.refresh()
        self.keep_bottom()

    # ---------- window plumbing ----------
    def keep_bottom(self):
        try:
            mp = getattr(self, "mpos", None)
            if mp:   # Windows can park an unmapped overrideredirect window at 0,0: check the real rect
                hw = ctypes.windll.user32.GetParent(self.mbox.winfo_id()) or self.mbox.winfo_id()
                rc = ctypes.wintypes.RECT()
                ctypes.windll.user32.GetWindowRect(hw, ctypes.byref(rc))
                if (rc.left, rc.top) != mp:
                    ctypes.windll.user32.SetWindowPos(hw, 1, mp[0], mp[1], 0, 0, 0x0011)  # NOSIZE|NOACTIVATE
            for w in (self.root, self.mbox):
                hwnd = ctypes.windll.user32.GetParent(w.winfo_id()) or w.winfo_id()
                ctypes.windll.user32.SetWindowPos(hwnd, 1, 0, 0, 0, 0, 0x0013)  # HWND_BOTTOM
        except Exception:
            pass
        self.root.after(1500, self.keep_bottom)

    def refresh(self):
        self.refresh_once()
        self.root.after(REFRESH_MS, self.refresh)

    def refresh_once(self):
        threading.Thread(target=self._load, daemon=True).start()

    def _load(self):
        try:
            rows, err = fetch()
        except Exception as e:  # noqa
            rows, err = None, str(e)
        self.root.after(0, self.render, rows, err)


    # ---------- system sensors ----------
    def start_sensors(self):
        try:
            self.proc = subprocess.Popen(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", SENSORS,
                 "-ParentPid", str(os.getpid()), "-Interval", "3"],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, creationflags=NOWIN,
                text=True, encoding="utf-8")
        except Exception:
            return

        def pump():
            for line in self.proc.stdout:
                try:
                    self.sens = json.loads(line)
                except ValueError:
                    continue
                self.root.after(0, self.draw_metrics)
        threading.Thread(target=pump, daemon=True).start()
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

    def quit(self):
        try:
            self.proc.kill()
        except Exception:
            pass
        self.root.destroy()

    def cell(self, c, x, y, w, label, value, pct, invert=False):
        c.create_text(x, y, text=label, font=self.f_cell, fill=DIM, anchor="nw", tags="m")
        c.create_text(x + w, y, text=value, font=self.f_cellv, fill=FG, anchor="ne", tags="m")
        by = y + self.f_cellv.metrics("linespace") + int(3 * S)
        bh = max(3, int(4 * S))
        c.create_rectangle(x, by, x + w, by + bh, fill=TRACK, outline="", tags="m")
        pct = max(0.0, min(100.0, pct or 0.0))
        if pct > 0:
            c.create_rectangle(x, by, x + max(2, int(w * pct / 100.0)), by + bh,
                               fill=level_colour(100 - pct if invert else pct), outline="", tags="m")

    def row_h(self):
        return self.f_cellv.metrics("linespace") + int(3 * S) + max(3, int(4 * S)) + int(12 * S)

    def metrics_height(self):
        head = self.f_head.metrics("linespace") + int(8 * S) + int(10 * S)
        return PAD + head + 3 * self.row_h() - int(10 * S) + PAD - int(4 * S)

    def draw_metrics(self):
        c = self.mcanvas
        c.delete("m")
        c.create_text(PAD, PAD, text="System", font=self.f_head, fill=FG, anchor="nw", tags="m")
        ly = PAD + self.f_head.metrics("linespace") + int(8 * S)
        c.create_line(PAD, ly, WIDTH - PAD, ly, fill=LINE, width=1, tags="m")
        y = ly + int(10 * S)
        gap = int(14 * S)
        w = (WIDTH - 2 * PAD - gap) // 2
        x1, x2 = PAD, PAD + w + gap
        row = self.row_h()
        t, cpu, gpu = self.sens.get("cpu_t"), self.sens.get("cpu"), self.sens.get("gpu")
        ctext = ("%d°C" % round(t) if t is not None else "--") + ("  %d%%" % round(cpu) if cpu is not None else "")
        self.cell(c, x1, y, w, "CPU", ctext, cpu)
        self.cell(c, x2, y, w, "GPU", "%d%%" % round(gpu) if gpu is not None else "--", gpu)
        ru, rt = ram_usage()
        self.cell(c, x1, y + row, w, "RAM", "%.1f/%.0f GB" % (ru, rt), ru / rt * 100)
        now = time.time()
        cur = net_octets()
        down = up = 0.0
        prev = getattr(self, "_net", None)
        if cur and prev and now > prev[0]:
            dt_ = now - prev[0]
            down = ((cur[0] - prev[1]) % 2 ** 32) / dt_
            up = ((cur[1] - prev[2]) % 2 ** 32) / dt_
        if cur:
            self._net = (now, cur[0], cur[1])
        self.cell(c, x2, y + row, w, "NET", "↓%s ↑%s" % (fmt_speed(down).replace("/s", ""), fmt_speed(up).replace("/s", "")),
                  min(100.0, max(down, up) / (12.5 * 1048576) * 100))
        # power: real battery rate when on battery, otherwise a load-based estimate
        dis, chg = self.sens.get("dis_w"), self.sens.get("chg_w")
        if dis:
            p_w, label, mark = dis, "POWER (battery)", ""
        else:
            p_w = 5.0 + 0.16 * (cpu or 0) + 0.05 * (gpu or 0)   # rough Ryzen-U estimate, screen excluded
            label, mark = "POWER (est.)", "~"
        self.cell(c, x1, y + 2 * row, w, label, "%s%.0f W" % (mark, p_w), min(100.0, p_w / 30.0 * 100))
        bat, ac = self.sens.get("bat"), self.sens.get("ac")
        btxt = ("%d%%" % bat if bat is not None else "--") + ("  AC" if ac else "")
        if chg:
            btxt += "  +%.0fW" % chg
        self.cell(c, x2, y + 2 * row, w, "BATTERY", btxt, 100 - (bat or 0) if False else (bat or 0), invert=True)

    def place_metrics(self, tasks_h):
        mh = self.metrics_height()
        my = Y + tasks_h + int(12 * S)
        self.mpos = (X, my)
        self.mgeom = "%dx%d+%d+%d" % (WIDTH, mh, X, my)
        self.mbox.geometry(self.mgeom)
        self.mcanvas.config(width=WIDTH, height=mh)
        png = self.glass(mh, X, my)
        self.mcanvas.delete("bg")
        if png:
            self.mbg = tk.PhotoImage(file=png)
            self.mcanvas.create_image(0, 0, anchor="nw", image=self.mbg, tags="bg")
            self.mcanvas.tag_lower("bg")
        self.draw_metrics()

    # ---------- glass background ----------
    def glass(self, h, x=X, y=Y):
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        out = os.path.join(CACHE, "flat_%d_%d_%d_%d_%d.png" % (sw, sh, x, y, h))
        os.makedirs(CACHE, exist_ok=True)
        if not os.path.exists(out):
            subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", RENDER,
                 "-Wallpaper", self.wall, "-ScreenW", str(sw), "-ScreenH", str(sh),
                 "-X", str(x), "-Y", str(y), "-W", str(WIDTH), "-H", str(h),
                 "-Radius", str(RADIUS), "-Thick", str(THICK), "-Out", out],
                creationflags=NOWIN, timeout=60, capture_output=True)
        return out if os.path.exists(out) else None

    # ---------- drawing ----------
    def render(self, rows, err):
        c = self.canvas
        c.delete("all")
        items = []
        y = PAD
        items.append(("t", PAD, y, "Tasks", self.f_head, FG, "nw", None))
        count = "" if rows is None else "%d open" % len(rows)
        items.append(("t", WIDTH - PAD, y + int(3 * S), count, self.f_count, DIM, "ne", None))
        y += self.f_head.metrics("linespace") + int(8 * S)
        items.append(("l", PAD, y, WIDTH - PAD, y))
        y += int(10 * S)
        text_x = PAD + int(30 * S)
        text_w = WIDTH - PAD - text_x
        if rows is None:
            for ln in wrap(self.f_due, "Not connected: " + err[:90], WIDTH - 2 * PAD):
                items.append(("t", PAD, y, ln, self.f_due, RED, "nw", None))
                y += self.f_due.metrics("linespace")
        elif not rows:
            items.append(("t", PAD, y, "All done ✓", self.f_title, GREEN, "nw", None))
            y += self.f_title.metrics("linespace")
        for tid, due, title in (rows or [])[:MAX_ROWS]:
            tag = "task_" + tid
            items.append(("t", PAD, y - int(2 * S), "○", self.f_circle, ACCENT, "nw", tag))
            for ln in wrap(self.f_title, title, text_w):
                items.append(("t", text_x, y, ln, self.f_title, FG, "nw", None))
                y += self.f_title.metrics("linespace")
            badge, colour = due_badge(due)
            if badge:
                items.append(("t", text_x, y, badge, self.f_due, colour, "nw", None))
                y += self.f_due.metrics("linespace")
            y += int(11 * S)
        h = max(y + PAD - int(4 * S), TALL_H)

        self.root.geometry("%dx%d+%d+%d" % (WIDTH, h, X, Y))
        c.config(width=WIDTH, height=h)
        png = self.glass(h)
        if png:
            self.bg_img = tk.PhotoImage(file=png)
            c.create_image(0, 0, anchor="nw", image=self.bg_img)
        for it in items:
            if it[0] == "l":
                c.create_line(it[1], it[2], it[3], it[4], fill=LINE, width=1)
            else:
                _, x, yy, text, font, colour, anchor, tag = it
                i = c.create_text(x, yy, text=text, font=font, fill=colour, anchor=anchor)
                if tag:
                    c.itemconfig(i, tags=(tag,))
                    c.tag_bind(tag, "<Button-1>", lambda e, t=tag[5:], i=i: self.done(t, i))
                    c.tag_bind(tag, "<Enter>", lambda e: c.config(cursor="hand2"))
                    c.tag_bind(tag, "<Leave>", lambda e: c.config(cursor=""))

        self.place_metrics(h)

    def done(self, tid, item):
        self.canvas.itemconfig(item, text="●", fill=GREEN)

        def work():
            run("done", tid)
            self.root.after(0, self.refresh_once)
        threading.Thread(target=work, daemon=True).start()


if __name__ == "__main__":
    Widget().root.mainloop()
