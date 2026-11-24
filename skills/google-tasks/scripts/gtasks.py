#!/usr/bin/env python3
"""Google Tasks CLI (stdlib only). Config/tokens live in %LOCALAPPDATA%/gtasks, never in G Drive.

  gtasks.py auth                         one-time browser login
  gtasks.py lists
  gtasks.py list [LIST] [--all]          LIST = title or id, default first list
  gtasks.py add TITLE [--list L] [--due YYYY-MM-DD] [--notes TEXT]
  gtasks.py done TASK_ID [--list L]
  gtasks.py delete TASK_ID [--list L]
  gtasks.py newlist TITLE
"""
import argparse, base64, hashlib, http.server, json, os, secrets, sys, time
import urllib.parse, urllib.request, urllib.error, webbrowser

DIR = os.path.join(os.environ.get("LOCALAPPDATA") or os.path.expanduser("~/.local/share"), "gtasks")
CRED, TOKEN = os.path.join(DIR, "credentials.json"), os.path.join(DIR, "token.json")
SCOPE = "https://www.googleapis.com/auth/tasks"
API = "https://tasks.googleapis.com/tasks/v1"
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save_token(t):
    with open(TOKEN, "w", encoding="utf-8") as f:
        json.dump(t, f)


def post_form(url, data):
    req = urllib.request.Request(url, urllib.parse.urlencode(data).encode())
    try:
        return json.load(urllib.request.urlopen(req, timeout=30))
    except urllib.error.HTTPError as e:
        sys.exit("token error: " + e.read().decode())


def client():
    if not os.path.exists(CRED):
        sys.exit("missing " + CRED + " - see SKILL.md setup")
    c = load(CRED)
    return c.get("installed") or c.get("web") or c


def auth():
    c = client()
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    got = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            got.update(urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query))
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("เชื่อมต่อสำเร็จ ปิดหน้านี้ได้".encode())

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    redirect = "http://127.0.0.1:%d" % srv.server_port
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": c["client_id"], "redirect_uri": redirect, "response_type": "code",
        "scope": SCOPE, "code_challenge": challenge, "code_challenge_method": "S256",
        "access_type": "offline", "prompt": "consent"})
    print("เปิดเบราว์เซอร์เพื่อ Authorize:\n" + url)
    webbrowser.open(url)
    while "code" not in got and "error" not in got:
        srv.handle_request()
    if "code" not in got:
        sys.exit("auth failed: %s" % got)
    t = post_form("https://oauth2.googleapis.com/token", {
        "client_id": c["client_id"], "client_secret": c.get("client_secret", ""),
        "code": got["code"][0], "code_verifier": verifier,
        "redirect_uri": redirect, "grant_type": "authorization_code"})
    t["expires_at"] = time.time() + t["expires_in"]
    save_token(t)
    print("auth ok")


def access_token():
    if not os.path.exists(TOKEN):
        sys.exit("not authorized - run: gtasks.py auth")
    t = load(TOKEN)
    if t["expires_at"] - 60 < time.time():
        c = client()
        n = post_form("https://oauth2.googleapis.com/token", {
            "client_id": c["client_id"], "client_secret": c.get("client_secret", ""),
            "refresh_token": t["refresh_token"], "grant_type": "refresh_token"})
        t.update(n)
        t["expires_at"] = time.time() + n["expires_in"]
        save_token(t)
    return t["access_token"]


def call(method, path, body=None, params=None):
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(
        url, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "Bearer " + access_token(), "Content-Type": "application/json"})
    try:
        r = urllib.request.urlopen(req, timeout=30).read()
    except urllib.error.HTTPError as e:
        sys.exit("API error %d: %s" % (e.code, e.read().decode()))
    return json.loads(r) if r else {}


def iter_items(path, params=None):
    """Read every API page; keep caller parameters unchanged."""
    query = dict(params or {})
    seen = set()
    while True:
        page = call("GET", path, params=query)
        yield from page.get("items", [])
        token = page.get("nextPageToken")
        if not token:
            return
        if token in seen:
            raise RuntimeError("API returned a repeated pagination token")
        seen.add(token)
        query["pageToken"] = token


def resolve(name):
    items = list(iter_items("/users/@me/lists", {"maxResults": 100}))
    if not items:
        sys.exit("no task lists")
    if not name:
        return items[0]["id"]
    # Prefer an exact ID; equal titles do not establish the intended target.
    for item in items:
        if name == item["id"]:
            return item["id"]
    matches = [item for item in items if name == item["title"]]
    if len(matches) == 1:
        return matches[0]["id"]
    if len(matches) > 1:
        sys.exit("ambiguous list title; use its ID: " + name)
    sys.exit("list not found: " + name)


def main():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("auth")
    sp.add_parser("lists")
    a = sp.add_parser("list")
    a.add_argument("list", nargs="?")
    a.add_argument("--all", action="store_true")
    a = sp.add_parser("add")
    a.add_argument("title")
    a.add_argument("--list")
    a.add_argument("--due")
    a.add_argument("--notes")
    for n in ("done", "delete"):
        a = sp.add_parser(n)
        a.add_argument("id")
        a.add_argument("--list")
    a = sp.add_parser("newlist")
    a.add_argument("title")
    o = p.parse_args()

    if o.cmd == "auth":
        os.makedirs(DIR, exist_ok=True)
        auth()
    elif o.cmd == "lists":
        for i in iter_items("/users/@me/lists", {"maxResults": 100}):
            print(i["id"], i["title"], sep="\t")
    elif o.cmd == "list":
        lid = resolve(o.list)
        params = {"maxResults": 100, "showCompleted": str(o.all).lower(), "showHidden": str(o.all).lower()}
        for t in iter_items("/lists/%s/tasks" % lid, params):
            mark = "x" if t["status"] == "completed" else " "
            print("[%s] %s\t%s\t%s" % (mark, t["id"], t.get("due", "")[:10], t.get("title", "")))
    elif o.cmd == "add":
        b = {"title": o.title}
        if o.due:
            b["due"] = o.due + "T00:00:00.000Z"
        if o.notes:
            b["notes"] = o.notes
        t = call("POST", "/lists/%s/tasks" % resolve(o.list), b)
        print("added", t["id"], t["title"])
    elif o.cmd == "done":
        call("PATCH", "/lists/%s/tasks/%s" % (resolve(o.list), o.id), {"status": "completed"})
        print("done")
    elif o.cmd == "delete":
        call("DELETE", "/lists/%s/tasks/%s" % (resolve(o.list), o.id))
        print("deleted")
    elif o.cmd == "newlist":
        print("created", call("POST", "/users/@me/lists", {"title": o.title})["id"])


if __name__ == "__main__":
    main()
