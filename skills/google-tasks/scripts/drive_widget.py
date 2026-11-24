"""Desktop widget: Google Drive sync status, same frosted-glass card size as the System card,
on the right side under the calendar card (cal_widget.py).

Run with pythonw (no console):  pythonw drive_widget.py
Stdlib only. Status is inferred from the Drive for desktop process (GoogleDriveFS.exe) I/O rate, the
account storage reported by the Drive-mounted drive, and the last write time of Drive's local database.
"""
import ctypes
import ctypes.wintypes
import datetime
import glob
import os
import shutil
import subprocess
import threading
import time
import tkinter as tk
import tkinter.font as tkfont

import tasks_widget as tw
import cal_widget as cw
from tasks_widget import _fs, S, PAD, WIDTH, FG, DIM, ACCENT, RED, AMBER, GREEN, LINE, FONT, NOWIN, KEY

GAP = int(12 * S)
INTERVAL = 3.0
BUSY_BPS = 100 * 1024          # above this I/O rate we call it "Syncing"
DRIVE_ROOT = os.environ.get("GDRIVE_LETTER", "G") + ":\\"
DB_GLOB = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google", "DriveFS", "*", "metadata_sqlite_db*")


class IoCounters(ctypes.Structure):
    _fields_ = [(n, ctypes.c_ulonglong) for n in (
        "ReadOps", "WriteOps", "OtherOps", "ReadBytes", "WriteBytes", "OtherBytes")]


def drive_pids():
    try:
        out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq GoogleDriveFS.exe", "/FO", "CSV", "/NH"],
                             capture_output=True, text=True, creationflags=NOWIN, timeout=15).stdout
    except Exception:
        return []
    pids = []
    for ln in out.splitlines():
        parts = [p.strip('"') for p in ln.split('","')]
        if len(parts) > 1 and parts[0].strip('"').lower() == "googledrivefs.exe":
            try:
                pids.append(int(parts[1]))
            except ValueError:
                pass
    return pids


def io_bytes(pids):
    total = 0
    k = ctypes.windll.kernel32
    for pid in pids:
        h = k.OpenProcess(0x1000, False, pid)      # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            continue
        c = IoCounters()
        if k.GetProcessIoCounters(h, ctypes.byref(c)):
            total += c.ReadBytes + c.WriteBytes
        k.CloseHandle(h)
    return total


def fmt_rate(bps):
    if bps >= 1024 * 1024:
        return "%.1f MB/s" % (bps / 1024.0 / 1024.0)
    if bps >= 1024:
        return "%d KB/s" % (bps / 1024)
    return "0 KB/s"


def ago(ts):
    s = max(0, time.time() - ts)
    if s < 90:
        return "just now"
    if s < 3600:
        return "%d min ago" % (s // 60)
    if s < 86400:
        return "%d hr ago" % (s // 3600)
    return "%d d ago" % (s // 86400)


class DriveWidget(tw.Widget):
    def __init__(self):
        r = self.root = tk.Tk()
        r.overrideredirect(True)
        r.configure(bg=KEY)
        r.attributes("-transparentcolor", KEY)
        r.attributes("-alpha", tw.ALPHA)
        self.X = r.winfo_screenwidth() - WIDTH - cw.MARGIN
        self.f_head = tkfont.Font(family=FONT, size=_fs(14), weight="bold")
        self.f_cell = tkfont.Font(family=FONT, size=_fs(9), weight="bold")
        self.f_cellv = tkfont.Font(family=FONT, size=_fs(10), weight="bold")
        self.H = self.metrics_height()
        self.Y = cw.Y + cw.TARGET_H + GAP
        r.geometry("%dx%d+%d+%d" % (WIDTH, self.H, self.X, self.Y))
        self.canvas = tk.Canvas(r, bg=KEY, highlightthickness=0, bd=0, width=WIDTH, height=self.H)
        self.canvas.pack(fill="both", expand=True)
        self.mbox = tk.Toplevel(r)       # keep_bottom() of the base class expects this
        self.mbox.withdraw()
        self.mpos = None
        self.wall = tw.wallpaper_path()
        self.info = {}
        self.prev = None
        self.bg_img = None
        png = tw.Widget.glass(self, self.H, self.X, self.Y)
        if png:
            self.bg_img = tk.PhotoImage(file=png)
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_img, tags="bg")
        threading.Thread(target=self.poll, daemon=True).start()
        self.draw()
        self.keep_bottom()

    def poll(self):
        while True:
            try:
                pids = drive_pids()
                now = time.time()
                b = io_bytes(pids) if pids else 0
                rate = 0.0
                if pids and self.prev and now > self.prev[0]:
                    rate = max(0.0, (b - self.prev[1]) / (now - self.prev[0]))
                self.prev = (now, b)
                try:
                    du = shutil.disk_usage(DRIVE_ROOT)
                    used, total = (du.total - du.free) / 1024 ** 3, du.total / 1024 ** 3
                except Exception:
                    used = total = None
                dbs = glob.glob(DB_GLOB)
                last = max((os.path.getmtime(p) for p in dbs), default=None)
                self.info = {"up": bool(pids), "rate": rate, "used": used, "total": total,
                             "last": last, "n": len(pids)}
            except Exception:
                pass
            self.root.after(0, self.draw)
            time.sleep(INTERVAL)

    def draw(self):
        c = self.canvas
        c.delete("m")
        i = self.info
        c.create_text(PAD, PAD, text="Google Drive", font=self.f_head, fill=FG, anchor="nw", tags="m")
        ly = PAD + self.f_head.metrics("linespace") + int(8 * S)
        c.create_line(PAD, ly, WIDTH - PAD, ly, fill=LINE, width=1, tags="m")
        y = ly + int(10 * S)
        gap = int(14 * S)
        w = (WIDTH - 2 * PAD - gap) // 2
        x1, x2 = PAD, PAD + w + gap
        row = self.row_h()
        if not i:
            return
        if not i["up"]:
            status, pct = "Not running", 8
        elif i["rate"] > BUSY_BPS:
            status, pct = "Syncing", 30
        else:
            status, pct = "Up to date", 100
        self.cell(c, x1, y, w, "STATUS", status, pct, invert=True)
        if i["used"] is not None:
            self.cell(c, x2, y, w, "USED", "%d/%d GB" % (i["used"], i["total"]), i["used"] / i["total"] * 100)
        else:
            self.cell(c, x2, y, w, "USED", "--", 0)
        self.cell(c, x1, y + row, w, "TRANSFER", fmt_rate(i["rate"]), min(100.0, i["rate"] / (5 * 1024 * 1024) * 100))
        self.cell(c, x2, y + row, w, "SYNCED", ago(i["last"]) if i["last"] else "--",
                  0, invert=True)
        self.cell(c, x1, y + 2 * row, w, "PROCESSES", str(i["n"]), min(100.0, i["n"] * 20.0))
        free = (i["total"] - i["used"]) if i["used"] is not None else None
        self.cell(c, x2, y + 2 * row, w, "FREE", "%d GB" % free if free is not None else "--",
                  (free / i["total"] * 100) if free is not None else 0, invert=True)
        c.tag_raise("m")


if __name__ == "__main__":
    DriveWidget().root.mainloop()
