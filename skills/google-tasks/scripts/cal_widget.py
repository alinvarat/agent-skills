"""Desktop widget: Google Calendar on the top-right of the desktop, same frosted-glass card as tasks_widget.py.

Run with pythonw (no console):  pythonw cal_widget.py
Data: %APPDATA%\\gcal-desktop-widget\\data.js, produced by update.ps1 from the calendar's secret iCal address
(config.json next to it). The widget re-runs update.ps1 every 10 minutes. Sits below normal windows.
"""
import calendar
import ctypes
import ctypes.wintypes
import datetime
import json
import os
import subprocess
import threading
import tkinter as tk
import tkinter.font as tkfont

import tasks_widget as tw
from tasks_widget import _fs, S, PAD, RADIUS, WIDTH, FG, DIM, ACCENT, RED, AMBER, LINE, FONT, NOWIN, KEY, wrap

DATA_DIR = os.path.join(os.environ.get("APPDATA", ""), "gcal-desktop-widget")
DATA = os.path.join(DATA_DIR, "data.js")
UPDATE = os.path.join(DATA_DIR, "update.ps1")
MARGIN = int(28 * S)
Y = int(64 * S)
MAX_DAYS = 2
TARGET_H = tw.TALL_H      # same card height as the Tasks card
TH_DAYS = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
TH_DAYS_S = ["จ.", "อ.", "พ.", "พฤ.", "ศ.", "ส.", "อา."]
TH_MONTHS = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม",
             "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]


def load_events():
    try:
        with open(DATA, encoding="utf-8-sig") as f:
            txt = f.read()
        obj = json.loads(txt[txt.index("{"):txt.rindex("}") + 1])
        evs = obj.get("events") or []
        if isinstance(evs, dict):
            evs = [evs]
        return evs
    except Exception:
        return None


def parse(s):
    return datetime.datetime.fromisoformat(s)


class CalWidget(tw.Widget):
    """Reuses the glass/bottom-window plumbing of the tasks widget, draws a calendar instead."""

    def __init__(self):
        r = self.root = tk.Tk()
        self.X = r.winfo_screenwidth() - WIDTH - MARGIN
        r.overrideredirect(True)
        r.configure(bg=KEY)
        r.attributes("-transparentcolor", KEY)
        r.attributes("-alpha", tw.ALPHA)
        r.geometry("%dx%d+%d+%d" % (WIDTH, 80, self.X, Y))
        self.canvas = tk.Canvas(r, bg=KEY, highlightthickness=0, bd=0, width=WIDTH, height=80)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-3>", lambda e: self.refresh_once(True))
        # tw.Widget.keep_bottom also touches a metrics box; give it a harmless hidden one
        self.mbox = tk.Toplevel(r)
        self.mbox.withdraw()
        self.mpos = None
        self.f_head = tkfont.Font(family=FONT, size=_fs(14), weight="bold")
        self.f_big = tkfont.Font(family=FONT, size=_fs(21), weight="bold")
        self.f_count = tkfont.Font(family=FONT, size=_fs(11))
        self.f_title = tkfont.Font(family=FONT, size=_fs(11), weight="bold")
        self.f_due = tkfont.Font(family=FONT, size=_fs(9), weight="bold")
        self.f_day = tkfont.Font(family=FONT, size=_fs(9), weight="bold")
        self.bg_img = None
        self.wall = tw.wallpaper_path()
        self.last_update = 0
        self.refresh()
        self.keep_bottom()

    def refresh(self):
        self.refresh_once()
        self.root.after(60 * 1000, self.refresh)

    def refresh_once(self, force=False):
        threading.Thread(target=self._load, args=(force,), daemon=True).start()

    def _load(self, force=False):
        import time
        if force or time.time() - self.last_update > 600:
            self.last_update = time.time()
            try:
                subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", UPDATE],
                               creationflags=NOWIN, timeout=90, capture_output=True)
            except Exception:
                pass
        self.root.after(0, self.render, load_events())

    def glass(self, h, x=None, y=None):
        return tw.Widget.glass(self, h, self.X, Y)

    def render(self, events):
        c = self.canvas
        c.delete("all")
        now = datetime.datetime.now()
        items = []
        y = PAD
        wd = TH_DAYS[now.weekday()]
        items.append(("t", PAD, y, "Calendar", self.f_head, FG, "nw"))
        items.append(("t", WIDTH - PAD, y + int(3 * S), wd, self.f_count, DIM, "ne"))
        y += self.f_head.metrics("linespace") + int(8 * S)
        items.append(("l", PAD, y, WIDTH - PAD, y))
        y += int(8 * S)
        items.append(("t", PAD, y, "%d %s %d" % (now.day, TH_MONTHS[now.month - 1], now.year + 543),
                      self.f_big, FG, "nw"))
        y += self.f_big.metrics("linespace") + int(10 * S)

        # ---- month grid (Sunday first) ----
        ev_days = set()
        for e in events or []:
            try:
                s0, e0 = parse(e["start"]).date(), parse(e["end"]).date()
            except Exception:
                continue
            if e.get("allDay") and e0 > s0:
                e0 -= datetime.timedelta(days=1)
            d = s0
            while d <= e0 and (d - s0).days < 40:
                ev_days.add(d)
                d += datetime.timedelta(days=1)
        cw = (WIDTH - 2 * PAD) / 7.0
        heads = ["อา", "จ", "อ", "พ", "พฤ", "ศ", "ส"]
        for i, hd in enumerate(heads):
            items.append(("t", PAD + cw * i + cw / 2, y, hd, self.f_day, ACCENT if i in (0, 6) else DIM, "n"))
        y += self.f_day.metrics("linespace") + int(4 * S)
        rh = self.f_title.metrics("linespace") + int(8 * S)
        for week in calendar.Calendar(firstweekday=6).monthdatescalendar(now.year, now.month):
            for i, d in enumerate(week):
                cx, cy = PAD + cw * i + cw / 2, y + rh / 2 - int(3 * S)
                if d == now.date():
                    r0 = int(13 * S)
                    items.append(("o", cx, cy, r0))
                col = "#1a1030" if d == now.date() else (FG if d.month == now.month else "#8b7fa8")
                items.append(("t", cx, cy, str(d.day), self.f_title, col, "center"))
                if d in ev_days and d != now.date():
                    items.append(("d", cx, cy + int(14 * S), int(2 * S)))
            y += rh
        y += int(4 * S)
        items.append(("l", PAD, y, WIDTH - PAD, y))
        y += int(6 * S)

        text_x = PAD + int(12 * S)
        text_w = WIDTH - PAD - text_x
        groups = {}
        for e in events or []:
            try:
                s, en = parse(e["start"]), parse(e["end"])
            except Exception:
                continue
            if not e.get("allDay") and en < now:
                continue
            groups.setdefault(s.date(), []).append((s, en, e))
        if events is None:
            for ln in wrap(self.f_due, "Calendar data not found. Run update.ps1.", WIDTH - 2 * PAD):
                items.append(("t", PAD, y, ln, self.f_due, RED, "nw"))
                y += self.f_due.metrics("linespace")
        elif not groups:
            items.append(("t", PAD, y, "ไม่มีนัดใน 30 วันข้างหน้า ✓", self.f_title, ACCENT, "nw"))
            y += self.f_title.metrics("linespace")
        full = False
        for day in sorted(groups)[:MAX_DAYS]:
            if full:
                break
            n = (day - now.date()).days
            label = "วันนี้" if n == 0 else ("พรุ่งนี้" if n == 1 else
                                              "%s %d %s" % (TH_DAYS_S[day.weekday()], day.day, TH_MONTHS[day.month - 1][:3] + "."))
            colour = RED if n == 0 else (AMBER if n <= 2 else DIM)
            first = sorted(groups[day], key=lambda g: g[0])[0][2]
            need0 = int(6 * S) + self.f_day.metrics("linespace") + int(3 * S)                 + len(wrap(self.f_title, first.get("title") or "", text_w)) * self.f_title.metrics("linespace")                 + self.f_due.metrics("linespace") + int(8 * S)
            if y + need0 + PAD > TARGET_H + int(8 * S):
                break
            y += int(6 * S)
            items.append(("t", PAD, y, label, self.f_day, colour, "nw"))
            y += self.f_day.metrics("linespace") + int(3 * S)
            for s, en, e in sorted(groups[day], key=lambda g: g[0]):
                need = len(wrap(self.f_title, e.get("title") or "", text_w)) * self.f_title.metrics("linespace")                     + self.f_due.metrics("linespace") + int(8 * S)
                if y + need + PAD > TARGET_H + int(8 * S):
                    full = True
                    break
                top = y
                for ln in wrap(self.f_title, e.get("title") or "(ไม่มีชื่อ)", text_w):
                    items.append(("t", text_x, y, ln, self.f_title, FG, "nw"))
                    y += self.f_title.metrics("linespace")
                tm = "ทั้งวัน" if e.get("allDay") else "%s – %s" % (s.strftime("%H:%M"), en.strftime("%H:%M"))
                if e.get("loc"):
                    tm += "  ·  " + e["loc"]
                for ln in wrap(self.f_due, tm, text_w):
                    items.append(("t", text_x, y, ln, self.f_due, DIM, "nw"))
                    y += self.f_due.metrics("linespace")
                items.append(("b", PAD, top, y))
                y += int(8 * S)
        h = TARGET_H

        self.root.geometry("%dx%d+%d+%d" % (WIDTH, h, self.X, Y))
        c.config(width=WIDTH, height=h)
        png = self.glass(h)
        if png:
            self.bg_img = tk.PhotoImage(file=png)
            c.create_image(0, 0, anchor="nw", image=self.bg_img)
        for it in items:
            if it[0] == "l":
                c.create_line(it[1], it[2], it[3], it[4], fill=LINE, width=1)
            elif it[0] == "o":
                c.create_oval(it[1] - it[3], it[2] - it[3], it[1] + it[3], it[2] + it[3], fill=ACCENT, outline="")
            elif it[0] == "d":
                c.create_oval(it[1] - it[3], it[2] - it[3], it[1] + it[3], it[2] + it[3], fill=ACCENT, outline="")
            elif it[0] == "b":
                c.create_rectangle(it[1], it[2] + 1, it[1] + max(2, int(3 * S)), it[3] - 1, fill=ACCENT, outline="")
            else:
                _, x, yy, text, font, colour, anchor = it
                c.create_text(x, yy, text=text, font=font, fill=colour, anchor=anchor)


if __name__ == "__main__":
    CalWidget().root.mainloop()
