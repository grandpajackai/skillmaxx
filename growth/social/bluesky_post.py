#!/usr/bin/env python3
"""Post due items from the SkillMaxx Bluesky queue via the AT Protocol.

Stdlib only. No LLM. Credentials are read from an env file and never printed.

Queue (merged, later files win on the same id):
  growth/social/bluesky-queue.json
  ~/.local/share/skillmaxx/bluesky-queue.local.json
State (posted URIs, daily cap):
  ~/.local/share/skillmaxx/bluesky-state.json

Credentials (chmod 600), first file that exists:
  $SKILLMAXX_BLUESKY_ENV, or ~/.skillmaxx-secrets/bluesky.env
Keys: BLUESKY_HANDLE, BLUESKY_APP_PASSWORD (alias: BLUESKY_SKILLMAXX_APP_PASSWORD).
Optional: BLUESKY_PDS (default https://bsky.social).

Usage:
  python3 growth/social/bluesky_post.py [--dry-run] [--list] [--mark-posted ID]
      [--queue PATH] [--state PATH] [--limit N] [--self-test]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ET = ZoneInfo("America/New_York")
DEFAULT_QUEUE = os.path.join(ROOT, "growth", "social", "bluesky-queue.json")
LOCAL_QUEUE = os.path.expanduser("~/.local/share/skillmaxx/bluesky-queue.local.json")
DEFAULT_STATE = os.path.expanduser("~/.local/share/skillmaxx/bluesky-state.json")
KEYFILE = os.path.expanduser(os.environ.get("SKILLMAXX_BLUESKY_ENV", "~/.skillmaxx-secrets/bluesky.env"))
DEFAULT_PDS = "https://bsky.social"
DEFAULT_HANDLE = "skillmaxx.bsky.social"
DAILY_CAP = 3
MAX_GRAPHEMES = 300
URL_RE = re.compile(r"https?://[^\s<>()]+", re.IGNORECASE)
TRAILING_PUNCT = ".,;:!?)]}>\"'"


def log(msg: str) -> None:
    print(msg, flush=True)


def atomic_write(path: str, data: str, mode: int = 0o600) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".tmp-", dir=os.path.dirname(path) or ".")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(data)
            if not data.endswith("\n"):
                f.write("\n")
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def load_json(path: str, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        log(f"warn: could not read {path}: {e.__class__.__name__}")
        return default


def parse_env_file(path: str) -> dict:
    env = {}
    if not os.path.exists(path):
        return env
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def credentials() -> dict:
    """Return handle/password/pds. Values are not logged by this function."""
    file_env = parse_env_file(KEYFILE)
    handle = (
        os.environ.get("BLUESKY_HANDLE")
        or file_env.get("BLUESKY_HANDLE")
        or DEFAULT_HANDLE
    )
    password = (
        os.environ.get("BLUESKY_APP_PASSWORD")
        or os.environ.get("BLUESKY_SKILLMAXX_APP_PASSWORD")
        or file_env.get("BLUESKY_APP_PASSWORD")
        or file_env.get("BLUESKY_SKILLMAXX_APP_PASSWORD")
        or ""
    )
    pds = (os.environ.get("BLUESKY_PDS") or file_env.get("BLUESKY_PDS") or DEFAULT_PDS).rstrip("/")
    return {"handle": handle, "password": password, "pds": pds, "keyfile_exists": os.path.exists(KEYFILE)}


def creds_ready(c: dict) -> bool:
    return bool(c.get("handle") and c.get("password"))


def parse_dt(s: str) -> datetime:
    s = (s or "").strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def load_queue(paths: list[str]) -> list[dict]:
    by_id = {}
    order = []
    for path in paths:
        doc = load_json(path, {})
        items = doc.get("items", doc) if isinstance(doc, dict) else doc
        if not isinstance(items, list):
            continue
        for it in items:
            if not isinstance(it, dict):
                continue
            iid = str(it.get("id") or "").strip()
            if not iid:
                iid = "anon-%s-%s" % (it.get("due_at") or "", hash(it.get("text") or "") & 0xFFFFFFFF)
                it = dict(it, id=iid)
            if iid not in by_id:
                order.append(iid)
            by_id[iid] = it
    items = [by_id[i] for i in order]
    items.sort(key=lambda x: parse_dt(str(x.get("due_at") or "9999-01-01T00:00:00+00:00")))
    return items


def load_state(path: str) -> dict:
    doc = load_json(path, {})
    if not isinstance(doc, dict):
        doc = {}
    posted = doc.get("posted") or []
    if not isinstance(posted, list):
        posted = []
    doc["posted"] = [p for p in posted if isinstance(p, dict)]
    return doc


def save_state(path: str, doc: dict) -> None:
    atomic_write(path, json.dumps(doc, indent=2, ensure_ascii=False) + "\n")


def canonical_text(s: str) -> str:
    """Compare text ignoring a leading http(s):// on URLs.

    Buffer/Bluesky often store the same post with a bare host, so an exact
    string match would miss a post that is already on the account feed.
    """
    return re.sub(r"https?://", "", (s or "").strip())


def posted_ids(state: dict) -> set[str]:
    return {str(p.get("id") or "") for p in state.get("posted") or [] if p.get("id")}


def posted_texts(state: dict) -> set[str]:
    return {canonical_text(p.get("text") or "") for p in state.get("posted") or [] if str(p.get("text") or "").strip()}


def posts_today(state: dict, now: datetime) -> int:
    day = now.astimezone(ET).date()
    n = 0
    for p in state.get("posted") or []:
        ts = p.get("posted_at") or ""
        try:
            if parse_dt(str(ts)).astimezone(ET).date() == day:
                n += 1
        except ValueError:
            continue
    return n


def trim_url(url: str) -> str:
    return url.rstrip(TRAILING_PUNCT)


def link_facets(text: str) -> list[dict]:
    """AT Protocol link facets using UTF-8 byte offsets."""
    facets = []
    for m in URL_RE.finditer(text):
        url = trim_url(m.group(0))
        if not url:
            continue
        start = len(text[: m.start()].encode("utf-8"))
        end = start + len(url.encode("utf-8"))
        facets.append({
            "index": {"byteStart": start, "byteEnd": end},
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": url}],
        })
    return facets


def first_url(text: str) -> str | None:
    m = URL_RE.search(text or "")
    return trim_url(m.group(0)) if m else None


def xrpc(pds: str, method: str, payload=None, body: bytes | None = None,
         token: str | None = None, content_type: str | None = None, timeout: int = 30):
    url = pds.rstrip("/") + "/xrpc/" + method
    headers = {}
    if token:
        headers["Authorization"] = "Bearer " + token
    data = None
    if body is not None:
        headers["Content-Type"] = content_type or "application/octet-stream"
        data = body
    elif payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            return json.loads(raw.decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"xrpc {method} failed: HTTP {e.code}") from None


def create_session(c: dict) -> dict:
    return xrpc(c["pds"], "com.atproto.server.createSession",
                payload={"identifier": c["handle"], "password": c["password"]})


def upload_blob(c: dict, token: str, path_or_url: str) -> dict:
    if path_or_url.startswith("https://") or path_or_url.startswith("http://"):
        req = urllib.request.Request(path_or_url, headers={"User-Agent": "SkillMaxxBluesky/1"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            ctype = resp.headers.get("Content-Type") or "application/octet-stream"
    else:
        path = path_or_url if os.path.isabs(path_or_url) else os.path.join(ROOT, path_or_url)
        with open(path, "rb") as f:
            data = f.read()
        ext = os.path.splitext(path)[1].lower()
        ctype = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                 ".webp": "image/webp", ".gif": "image/gif"}.get(ext, "application/octet-stream")
    return xrpc(c["pds"], "com.atproto.repo.uploadBlob", body=data, token=token, content_type=ctype)


def author_texts(c: dict, token: str, actor: str, limit: int = 20) -> set[str]:
    q = urllib.parse.urlencode({"actor": actor, "limit": str(limit)})
    url = c["pds"].rstrip("/") + "/xrpc/app.bsky.feed.getAuthorFeed?" + q
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            feed = json.loads(resp.read().decode("utf-8")).get("feed") or []
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError):
        return set()
    out = set()
    for row in feed:
        text = (((row.get("post") or {}).get("record") or {}).get("text") or "").strip()
        if text:
            out.add(canonical_text(text))
            out.add(text)
    return out


def build_record(text: str, images: list[dict] | None = None) -> dict:
    rec = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "langs": ["en"],
    }
    facets = link_facets(text)
    if facets:
        rec["facets"] = facets
    if images:
        rec["embed"] = {"$type": "app.bsky.embed.images", "images": images[:4]}
    return rec


def item_images(item: dict) -> list:
    imgs = item.get("images") or []
    if isinstance(imgs, str):
        imgs = [imgs]
    return [i for i in imgs if i]


def classify(item: dict, state: dict, now: datetime, feed_texts: set[str] | None = None) -> str:
    """Return a skip reason, or 'due' if it should post."""
    iid = str(item.get("id") or "")
    text = str(item.get("text") or "").strip()
    if not text:
        return "empty text"
    if iid and iid in posted_ids(state):
        return "already in state"
    if canonical_text(text) in posted_texts(state):
        return "text already in state"
    if feed_texts is not None and canonical_text(text) in feed_texts:
        return "already on account feed"
    try:
        due = parse_dt(str(item.get("due_at") or ""))
    except ValueError:
        return "bad due_at"
    if due > now:
        return "not due yet"
    if len(text) > MAX_GRAPHEMES:
        return f"text over {MAX_GRAPHEMES} graphemes"
    return "due"


def post_item(c: dict, session: dict, item: dict) -> dict:
    token = session["accessJwt"]
    did = session["did"]
    text = str(item.get("text") or "").strip()
    images = []
    alts = item.get("alt") or item.get("alts") or []
    if isinstance(alts, str):
        alts = [alts]
    for i, src in enumerate(item_images(item)):
        blob = upload_blob(c, token, src)
        alt = alts[i] if i < len(alts) else (item.get("alt_text") or "")
        images.append({"alt": str(alt or ""), "image": blob["blob"]})
    rec = build_record(text, images or None)
    return xrpc(c["pds"], "com.atproto.repo.createRecord", token=token, payload={
        "repo": did,
        "collection": "app.bsky.feed.post",
        "record": rec,
    })


def fmt_due(item: dict) -> str:
    try:
        return parse_dt(str(item["due_at"])).astimezone(ET).strftime("%Y-%m-%d %I:%M %p ET")
    except Exception:
        return str(item.get("due_at") or "?")


def preview(item: dict) -> str:
    text = re.sub(r"\s+", " ", str(item.get("text") or "")).strip()
    if len(text) > 140:
        text = text[:137] + "..."
    return text


def run_list(items: list[dict], state: dict, now: datetime) -> int:
    log(f"queue: {len(items)} item(s); posted in state: {len(state.get('posted') or [])}; "
        f"today ({now.astimezone(ET).date().isoformat()} ET): {posts_today(state, now)}/{DAILY_CAP}")
    for it in items:
        reason = classify(it, state, now)
        log(f"  [{it.get('id')}] {fmt_due(it)}  {reason}  {preview(it)}")
    return 0


def mark_posted(state_path: str, items: list[dict], iid: str, now: datetime) -> int:
    state = load_state(state_path)
    if iid in posted_ids(state):
        log(f"{iid}: already in state")
        return 0
    item = next((x for x in items if str(x.get("id") or "") == iid), None)
    if not item:
        log(f"{iid}: not in queue")
        return 1
    state.setdefault("posted", []).append({
        "id": iid,
        "text": str(item.get("text") or "").strip(),
        "uri": "",
        "posted_at": now.astimezone(timezone.utc).isoformat(),
        "note": "marked by --mark-posted (e.g. already published via Buffer)",
    })
    save_state(state_path, state)
    log(f"{iid}: recorded in state (no Bluesky post was made)")
    return 0


def run_self_test() -> int:
    text = "See the report: https://skillmaxx.gilventures.ai/reports/2026-11-14/ thanks."
    facets = link_facets(text)
    assert len(facets) == 1, facets
    url = first_url(text)
    assert url == "https://skillmaxx.gilventures.ai/reports/2026-11-14/"
    start, end = facets[0]["index"]["byteStart"], facets[0]["index"]["byteEnd"]
    assert text.encode("utf-8")[start:end].decode("utf-8") == url
    # punctuation trimmed, emoji / non-ascii prefix shifts byte offsets
    text2 = "café https://example.com/a."
    f2 = link_facets(text2)
    start, end = f2[0]["index"]["byteStart"], f2[0]["index"]["byteEnd"]
    assert text2.encode("utf-8")[start:end].decode() == "https://example.com/a"
    now = datetime(2026, 11, 21, 20, 0, tzinfo=timezone.utc)
    items = [
        {"id": "future", "text": "later", "due_at": "2026-11-22T00:00:00+00:00"},
        {"id": "due1", "text": "now one https://skillmaxx.gilventures.ai/", "due_at": "2026-11-21T19:00:00+00:00"},
        {"id": "due2", "text": "now two", "due_at": "2026-11-21T19:30:00+00:00"},
    ]
    state = {"posted": [{"id": "due2", "text": "now two", "posted_at": "2026-11-21T19:31:00+00:00"}]}
    assert classify(items[0], state, now) == "not due yet"
    assert classify(items[1], state, now) == "due"
    assert classify(items[2], state, now) == "already in state"
    assert posts_today(state, now) == 1
    # Bluesky often stores the same post with a bare host (no https://).
    url_item = {"id": "url1", "text": "See https://skillmaxx.gilventures.ai/how-we-test/",
                "due_at": "2026-11-21T19:00:00+00:00"}
    bare = "See skillmaxx.gilventures.ai/how-we-test/"
    assert classify(url_item, {"posted": []}, now, {canonical_text(bare)}) == "already on account feed"
    assert classify(url_item, {"posted": [{"id": "x", "text": bare, "posted_at": "2026-11-21T19:00:00+00:00"}]}, now) == "text already in state"
    log("self-test ok")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="print what would post; never contact Bluesky")
    ap.add_argument("--list", action="store_true", help="show queue status and exit")
    ap.add_argument("--mark-posted", metavar="ID", help="record a queue id as already posted (no network)")
    ap.add_argument("--queue", action="append", default=[], help="extra queue JSON (repeatable)")
    ap.add_argument("--state", default=DEFAULT_STATE, help="state JSON path")
    ap.add_argument("--limit", type=int, default=0, help="max posts this run (after the daily cap)")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        return run_self_test()

    now = datetime.now(timezone.utc)
    paths = [DEFAULT_QUEUE, LOCAL_QUEUE] + list(args.queue or [])
    items = load_queue(paths)
    state = load_state(args.state)

    if args.list:
        return run_list(items, state, now)
    if args.mark_posted:
        return mark_posted(args.state, items, args.mark_posted, now)

    c = credentials()
    has_creds = creds_ready(c)
    # Never print secret values or whether a particular alias was used.
    if c.get("keyfile_exists"):
        cred_note = f"keyfile present at {KEYFILE} (contents not printed)"
    elif has_creds:
        cred_note = "app password present in the environment (value not printed)"
    else:
        cred_note = f"no app password (looked at {KEYFILE} and env aliases; values never printed)"

    log(f"bluesky_post: {'DRY-RUN' if args.dry_run else 'live'}  items={len(items)}  {cred_note}")
    used = posts_today(state, now)
    log(f"daily cap: {used}/{DAILY_CAP} already posted today (America/New_York)")

    feed_texts = None
    session = None
    if not args.dry_run:
        if not has_creds:
            log("no credentials; nothing posted (safe no-op). Add a chmod 600 keyfile to post.")
            run_list(items, state, now)
            return 0
        try:
            session = create_session(c)
            feed_texts = author_texts(c, session["accessJwt"], session.get("did") or c["handle"])
        except Exception as e:
            log(f"login or feed fetch failed: {e}")
            return 2

    posted = 0
    for it in items:
        reason = classify(it, state, now, feed_texts)
        tag = f"[{it.get('id')}] {fmt_due(it)}"
        if reason != "due":
            log(f"skip {tag}: {reason}")
            continue
        if used + posted >= DAILY_CAP:
            log(f"skip {tag}: daily cap of {DAILY_CAP} reached")
            continue
        if args.limit and posted >= args.limit:
            log(f"skip {tag}: --limit {args.limit} reached")
            continue
        if args.dry_run:
            log(f"would post {tag}: {preview(it)}")
            posted += 1
            continue
        try:
            res = post_item(c, session, it)
        except Exception as e:
            log(f"FAIL {tag}: {e}")
            return 2
        uri = res.get("uri") or ""
        state.setdefault("posted", []).append({
            "id": it.get("id"),
            "text": str(it.get("text") or "").strip(),
            "uri": uri,
            "cid": res.get("cid") or "",
            "posted_at": now.astimezone(timezone.utc).isoformat(),
        })
        save_state(args.state, state)
        # Public AT URI only (no tokens).
        log(f"posted {tag}: {uri}")
        posted += 1
        now = datetime.now(timezone.utc)
    log(f"bluesky_post: {'would post' if args.dry_run else 'posted'} {posted}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
