#!/usr/bin/env python3
"""Zoho Mail REST helper for skillmaxx@gilventures.ai. No secrets in this file.

Credentials are read from $ZOHO_CREDS (default /home/box/.skillmaxx-secrets/zoho_skillmaxx.json),
a JSON file with client_id, client_secret, refresh_token. Values are never printed.

Usage:
  zoho_mail.py folders                              list folders (incl. Spam) with ids
  zoho_mail.py list FOLDER [--limit N]              list messages in a folder (name or id)
  zoho_mail.py search "SEARCHKEY" [--limit N]       Zoho search syntax, e.g. "sender:weaviate.io"
  zoho_mail.py find TEXT [--folders Inbox,Spam,Sent] list messages whose from/to/subject contains TEXT
  zoho_mail.py content FOLDER_ID MESSAGE_ID         print a message body (html)
  zoho_mail.py send --to A --subject S (--body-file F | --body TEXT) [--html] [--cc C] [--dry-run]
  zoho_mail.py reply MESSAGE_ID --to A --subject S (--body-file F | --body TEXT) [--html] [--dry-run]
       reply threads the message on MESSAGE_ID (a message in Inbox or Sent) via action=reply.

Sending is an outside action: only send what Brandon approved.
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request, html as htmlmod

CREDS = os.environ.get("ZOHO_CREDS", "/home/box/.skillmaxx-secrets/zoho_skillmaxx.json")
ACCOUNT = os.environ.get("ZOHO_ACCOUNT_ID", "7217576000000008002")
FROM = os.environ.get("ZOHO_FROM", "Brandon at SkillMaxx <skillmaxx@gilventures.ai>")
API = f"https://mail.zoho.com/api/accounts/{ACCOUNT}"
TOKEN_URL = "https://accounts.zoho.com/oauth/v2/token"
CACHE = os.path.join(os.path.dirname(CREDS), ".zoho_access_token.json")

def _http(method, url, body=None, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        txt = e.read().decode(errors="replace")
        try: return e.code, json.loads(txt)
        except Exception: return e.code, {"raw": txt[:500]}

def token(force=False):
    if not force and os.path.exists(CACHE):
        c = json.load(open(CACHE))
        if c.get("exp", 0) > time.time() + 60: return c["access_token"]
    c = json.load(open(CREDS))
    q = urllib.parse.urlencode({"refresh_token": c["refresh_token"], "client_id": c["client_id"],
                                "client_secret": c["client_secret"], "grant_type": "refresh_token"})
    st, j = _http("POST", f"{TOKEN_URL}?{q}")
    if st != 200 or "access_token" not in j:
        sys.exit(f"token refresh failed: HTTP {st} {j.get('error', '')}")
    fd = os.open(CACHE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump({"access_token": j["access_token"], "exp": time.time() + int(j.get("expires_in", 3600))}, f)
    return j["access_token"]

def call(method, path, body=None, params=None):
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    for attempt in range(2):
        h = {"Authorization": "Zoho-oauthtoken " + token(force=attempt > 0), "Accept": "application/json"}
        if body is not None: h["Content-Type"] = "application/json"
        st, j = _http(method, url, body, h)
        if st != 401: return st, j
    return st, j

def folders():
    st, j = call("GET", "/folders")
    if st != 200: sys.exit(f"folders failed: HTTP {st} {j}")
    return j["data"]

def folder_id(name):
    if str(name).isdigit(): return str(name)
    for f in folders():
        if f["folderName"].lower() == name.lower() or f.get("folderType", "").lower() == name.lower():
            return f["folderId"]
    sys.exit(f"no folder {name}")

def list_folder(name, limit=200):
    fid, out, start = folder_id(name), [], 1
    while True:
        st, j = call("GET", "/messages/view", params={"folderId": fid, "start": start, "limit": min(100, limit - len(out)), "includeto": "true"})
        if st != 200: sys.exit(f"list failed: HTTP {st} {j}")
        d = j.get("data", []); out += d
        if len(d) < 100 or len(out) >= limit: return out
        start += 100

def search(key, limit=200):
    st, j = call("GET", "/messages/search", params={"searchKey": key, "limit": limit, "includeto": "true",
                                                    "receivedTime": int(time.time() * 1000) + 60000})
    if st != 200: sys.exit(f"search failed: HTTP {st} {j}")
    return j.get("data", [])

def content(fid, mid):
    st, j = call("GET", f"/folders/{fid}/messages/{mid}/content")
    if st != 200: sys.exit(f"content failed: HTTP {st} {j}")
    return j["data"].get("content", "")

def _body(a):
    b = open(a.body_file).read() if a.body_file else a.body
    if a.html: return b, "html"
    return b, "plaintext"

def send(to, subject, body, fmt="plaintext", cc=None, reply_to_mid=None):
    p = {"fromAddress": FROM, "toAddress": to, "subject": subject, "content": body, "mailFormat": fmt}
    if cc: p["ccAddress"] = cc
    if reply_to_mid:
        p["action"] = "reply"
        return call("POST", f"/messages/{reply_to_mid}", p)
    return call("POST", "/messages", p)

def show(ms):
    for m in ms:
        t = time.strftime("%Y-%m-%d %H:%M", time.localtime(int(m.get("receivedTime") or m.get("sentDateInGMT") or 0) / 1000))
        print(f"{t}  f={m.get('folderId')} m={m.get('messageId')}  from={m.get('fromAddress')}  to={htmlmod.unescape(m.get('toAddress') or '')[:60]}  {m.get('subject')}")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("folders")
    p = sp.add_parser("list"); p.add_argument("folder"); p.add_argument("--limit", type=int, default=50)
    p = sp.add_parser("search"); p.add_argument("key"); p.add_argument("--limit", type=int, default=50)
    p = sp.add_parser("find"); p.add_argument("text"); p.add_argument("--folders", default="Inbox,Spam,Sent")
    p = sp.add_parser("content"); p.add_argument("fid"); p.add_argument("mid")
    for n in ("send", "reply"):
        p = sp.add_parser(n)
        if n == "reply": p.add_argument("mid")
        p.add_argument("--to", required=True); p.add_argument("--subject", required=True); p.add_argument("--cc")
        p.add_argument("--body"); p.add_argument("--body-file"); p.add_argument("--html", action="store_true"); p.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.cmd == "folders":
        for f in folders(): print(f"{f['folderId']}  {f['folderName']}  ({f.get('folderType', '')})")
    elif a.cmd == "list": show(list_folder(a.folder, a.limit))
    elif a.cmd == "search": show(search(a.key, a.limit))
    elif a.cmd == "find":
        t = a.text.lower()
        for fn in a.folders.split(","):
            show([m for m in list_folder(fn, 1000) if t in " ".join(str(m.get(k, "")) for k in ("fromAddress", "toAddress", "subject", "sender")).lower()])
    elif a.cmd == "content": print(content(a.fid, a.mid))
    else:
        body, fmt = _body(a)
        if a.dry_run: print(f"DRY RUN {a.cmd} to={a.to} subject={a.subject!r} fmt={fmt} chars={len(body)}"); return
        st, j = send(a.to, a.subject, body, fmt, a.cc, getattr(a, "mid", None))
        print(f"HTTP {st} {j.get('status', {}).get('description', '')} messageId={j.get('data', {}).get('messageId', '')}")
        if st != 200: sys.exit(1)

if __name__ == "__main__":
    main()
