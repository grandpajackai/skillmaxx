#!/usr/bin/env python3
"""SkillMaxx Bluesky / AT Protocol helpers (stdlib only).

Login, reply, like, follow, unfollow, and list notifications via XRPC.
Credentials are read from an env file and never printed. Session tokens
are never logged or written to stdout.

Credentials (chmod 600), first file that exists:
  $SKILLMAXX_BLUESKY_ENV, or ~/.skillmaxx-secrets/bluesky.env
Keys: BLUESKY_HANDLE, BLUESKY_APP_PASSWORD (alias: BLUESKY_SKILLMAXX_APP_PASSWORD).
Optional: BLUESKY_PDS (default https://bsky.social).

Usage:
  python3 growth/bluesky/bsky_api.py login
  python3 growth/bluesky/bsky_api.py profile HANDLE
  python3 growth/bluesky/bsky_api.py thread URL
  python3 growth/bluesky/bsky_api.py reply URL TEXT
  python3 growth/bluesky/bsky_api.py like URL
  python3 growth/bluesky/bsky_api.py follow HANDLE
  python3 growth/bluesky/bsky_api.py unfollow HANDLE
  python3 growth/bluesky/bsky_api.py notifications [--since ISO] [--limit N]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

DEFAULT_PDS = "https://bsky.social"
DEFAULT_HANDLE = "skillmaxx.bsky.social"
KEYFILE = os.path.expanduser(
    os.environ.get("SKILLMAXX_BLUESKY_ENV", "~/.skillmaxx-secrets/bluesky.env")
)
MAX_GRAPHEMES = 300
URL_RE = re.compile(r"https?://[^\s<>()]+", re.IGNORECASE)
TRAILING_PUNCT = ".,;:!?)]}>\"'"
BSKY_POST_RE = re.compile(
    r"(?:https?://)?(?:bsky\.app|main\.bsky\.dev)/profile/([^/]+)/post/([A-Za-z0-9._~-]+)",
    re.IGNORECASE,
)
AT_POST_RE = re.compile(
    r"^at://([^/]+)/app\.bsky\.feed\.post/([A-Za-z0-9._~-]+)$"
)
# Do not log values that look like JWTs, app passwords, or session tokens.
SECRET_KEY_RE = re.compile(
    r"(password|passwd|secret|token|jwt|authorization|accessjwt|refreshjwt|app.?password)",
    re.IGNORECASE,
)
JWTISH_RE = re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")


def log(msg: str) -> None:
    print(sanitize(msg), flush=True)


def sanitize(text: str) -> str:
    return JWTISH_RE.sub("[redacted-token]", text or "")


def redact_obj(obj, depth: int = 0):
    """Return a copy of obj with secret-looking keys and JWT values removed."""
    if depth > 8:
        return "<max-depth>"
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if SECRET_KEY_RE.search(str(k)):
                out[k] = "[redacted]"
            else:
                out[k] = redact_obj(v, depth + 1)
        return out
    if isinstance(obj, list):
        return [redact_obj(v, depth + 1) for v in obj]
    if isinstance(obj, str):
        return sanitize(obj)
    return obj


def grapheme_count(text: str) -> int:
    try:
        import regex  # type: ignore

        return len(regex.findall(r"\X", text))
    except ImportError:
        return len(text)


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
    return {
        "handle": handle,
        "password": password,
        "pds": pds,
        "keyfile_exists": os.path.exists(KEYFILE),
    }


def creds_ready(c: dict) -> bool:
    return bool(c.get("handle") and c.get("password"))


def creds_note(c: dict) -> str:
    if c.get("keyfile_exists"):
        return f"keyfile present at {KEYFILE} (contents not printed)"
    if creds_ready(c):
        return "app password present in the environment (value not printed)"
    return f"no app password (looked at {KEYFILE} and env aliases; values never printed)"


def _error_summary(raw: str) -> str:
    raw = sanitize((raw or "").strip())
    try:
        doc = json.loads(raw)
    except ValueError:
        return raw[:200]
    if not isinstance(doc, dict):
        return raw[:200]
    err = str(doc.get("error") or "")
    msg = sanitize(str(doc.get("message") or ""))
    parts = [p for p in (err, msg) if p]
    return ": ".join(parts)[:200] if parts else raw[:200]


def xrpc(
    pds: str,
    method: str,
    payload=None,
    token: str | None = None,
    params: dict | None = None,
    timeout: int = 30,
    http_method: str | None = None,
):
    url = pds.rstrip("/") + "/xrpc/" + method
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    headers = {}
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")
    if token:
        headers["Authorization"] = "Bearer " + token
    verb = http_method or ("POST" if data is not None else "GET")
    req = urllib.request.Request(url, data=data, headers=headers, method=verb)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            return json.loads(raw.decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"xrpc {method} failed: HTTP {e.code} {_error_summary(err)}") from None


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


def parse_post_ref(url_or_uri: str) -> tuple[str, str]:
    """Return (handle_or_did, rkey) from a bsky.app URL or at:// URI."""
    s = (url_or_uri or "").strip()
    m = AT_POST_RE.match(s)
    if m:
        return m.group(1), m.group(2)
    m = BSKY_POST_RE.search(s)
    if m:
        return urllib.parse.unquote(m.group(1)), m.group(2)
    raise ValueError(f"not a Bluesky post URL or AT URI: {s}")


def public_post_url(handle_or_did: str, rkey: str) -> str:
    return f"https://bsky.app/profile/{handle_or_did}/post/{rkey}"


def uri_rkey(uri: str) -> str:
    return (uri or "").rstrip("/").split("/")[-1]


def at_uri_url(uri: str, handle: str | None = None) -> str:
    if not uri:
        return ""
    try:
        actor, rkey = parse_post_ref(uri)
    except ValueError:
        return uri
    return public_post_url(handle or actor, rkey)


class Client:
    """Logged-in AT Protocol client. Tokens stay on this object and are never printed."""

    def __init__(self, creds: dict | None = None):
        self.creds = creds or credentials()
        self.pds = self.creds["pds"]
        self.handle = self.creds["handle"]
        self.did = ""
        self._access = ""
        self._refresh = ""

    def login(self) -> dict:
        if not creds_ready(self.creds):
            raise RuntimeError("no Bluesky credentials; " + creds_note(self.creds))
        sess = xrpc(
            self.pds,
            "com.atproto.server.createSession",
            payload={"identifier": self.creds["handle"], "password": self.creds["password"]},
        )
        self._access = sess.get("accessJwt") or ""
        self._refresh = sess.get("refreshJwt") or ""
        self.did = sess.get("did") or ""
        self.handle = sess.get("handle") or self.handle
        if not self._access or not self.did:
            raise RuntimeError("createSession did not return a session (details not printed)")
        return {"handle": self.handle, "did": self.did, "pds": self.pds}

    def _token(self) -> str:
        if not self._access:
            raise RuntimeError("not logged in")
        return self._access

    def get(self, method: str, params: dict | None = None):
        return xrpc(self.pds, method, token=self._token(), params=params)

    def post(self, method: str, payload: dict):
        return xrpc(self.pds, method, payload=payload, token=self._token())

    def resolve_handle(self, handle: str) -> str:
        handle = (handle or "").lstrip("@").strip()
        if handle.startswith("did:"):
            return handle
        doc = xrpc(
            self.pds,
            "com.atproto.identity.resolveHandle",
            params={"handle": handle},
            token=self._access or None,
        )
        did = doc.get("did") or ""
        if not did:
            raise RuntimeError(f"could not resolve handle {handle}")
        return did

    def post_uri(self, url_or_uri: str) -> str:
        actor, rkey = parse_post_ref(url_or_uri)
        if actor.startswith("did:"):
            did = actor
        else:
            did = self.resolve_handle(actor)
        return f"at://{did}/app.bsky.feed.post/{rkey}"

    def get_profile(self, actor: str) -> dict:
        actor = (actor or "").lstrip("@").strip()
        return self.get("app.bsky.actor.getProfile", {"actor": actor})

    def get_thread(self, url_or_uri: str, depth: int = 10) -> dict:
        uri = url_or_uri if url_or_uri.startswith("at://") else self.post_uri(url_or_uri)
        doc = self.get("app.bsky.feed.getPostThread", {"uri": uri, "depth": str(depth)})
        return doc.get("thread") or {}

    def thread_post(self, url_or_uri: str, depth: int = 10) -> dict:
        thread = self.get_thread(url_or_uri, depth=depth)
        if thread.get("$type") == "app.bsky.feed.defs#notFoundPost":
            raise RuntimeError(f"post not found: {url_or_uri}")
        post = thread.get("post") or {}
        if not post.get("uri"):
            raise RuntimeError(f"could not load post: {url_or_uri}")
        return post

    def reply_refs(self, url_or_uri: str) -> dict:
        """Root/parent refs for a reply to this post."""
        post = self.thread_post(url_or_uri, depth=0)
        uri = post["uri"]
        cid = post["cid"]
        parent = {"uri": uri, "cid": cid}
        rec = post.get("record") or {}
        existing = (rec.get("reply") or {}).get("root") or {}
        root = {"uri": existing["uri"], "cid": existing["cid"]} if existing.get("uri") and existing.get("cid") else parent
        return {"root": root, "parent": parent}

    def already_replied(self, url_or_uri: str, author_did: str | None = None) -> dict | None:
        """Return our direct reply post if one already exists on this post."""
        author_did = author_did or self.did
        thread = self.get_thread(url_or_uri, depth=3)
        parent_uri = (thread.get("post") or {}).get("uri") or ""
        for item in thread.get("replies") or []:
            post = item.get("post") or {}
            rec = post.get("record") or {}
            reply = rec.get("reply") or {}
            parent = (reply.get("parent") or {}).get("uri") or ""
            did = ((post.get("author") or {}).get("did") or "")
            if did == author_did and (parent == parent_uri or not parent):
                return post
        return None

    def already_liked(self, url_or_uri: str) -> str:
        post = self.thread_post(url_or_uri, depth=0)
        return ((post.get("viewer") or {}).get("like") or "") or ""

    def already_following(self, actor: str) -> str:
        prof = self.get_profile(actor)
        return ((prof.get("viewer") or {}).get("following") or "") or ""

    def create_post(self, text: str, reply: dict | None = None) -> dict:
        text = (text or "").strip()
        if not text:
            raise ValueError("empty post text")
        n = grapheme_count(text)
        if n > MAX_GRAPHEMES:
            raise ValueError(f"text is {n} graphemes (limit {MAX_GRAPHEMES})")
        rec = {
            "$type": "app.bsky.feed.post",
            "text": text,
            "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "langs": ["en"],
        }
        facets = link_facets(text)
        if facets:
            rec["facets"] = facets
        if reply:
            rec["reply"] = reply
        res = self.post("com.atproto.repo.createRecord", {
            "repo": self.did,
            "collection": "app.bsky.feed.post",
            "record": rec,
        })
        return res

    def reply(self, url_or_uri: str, text: str, skip_if_replied: bool = True) -> dict:
        existing = self.already_replied(url_or_uri) if skip_if_replied else None
        if existing:
            uri = existing.get("uri") or ""
            handle = ((existing.get("author") or {}).get("handle") or self.handle)
            return {
                "skipped": "already replied",
                "uri": uri,
                "url": at_uri_url(uri, handle),
            }
        refs = self.reply_refs(url_or_uri)
        res = self.create_post(text, reply=refs)
        uri = res.get("uri") or ""
        return {
            "uri": uri,
            "cid": res.get("cid") or "",
            "url": at_uri_url(uri, self.handle),
        }

    def like(self, url_or_uri: str, skip_if_liked: bool = True) -> dict:
        post = self.thread_post(url_or_uri, depth=0)
        existing = ((post.get("viewer") or {}).get("like") or "") or ""
        if skip_if_liked and existing:
            return {"skipped": "already liked", "uri": existing}
        res = self.post("com.atproto.repo.createRecord", {
            "repo": self.did,
            "collection": "app.bsky.feed.like",
            "record": {
                "$type": "app.bsky.feed.like",
                "subject": {"uri": post["uri"], "cid": post["cid"]},
                "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            },
        })
        return {"uri": res.get("uri") or "", "cid": res.get("cid") or ""}

    def follow(self, actor: str, skip_if_following: bool = True) -> dict:
        actor = (actor or "").lstrip("@").strip()
        prof = self.get_profile(actor)
        existing = ((prof.get("viewer") or {}).get("following") or "") or ""
        if skip_if_following and existing:
            return {
                "skipped": "already following",
                "uri": existing,
                "did": prof.get("did") or "",
                "handle": prof.get("handle") or actor,
            }
        did = prof.get("did") or ""
        if not did:
            raise RuntimeError(f"could not resolve profile for {actor}")
        res = self.post("com.atproto.repo.createRecord", {
            "repo": self.did,
            "collection": "app.bsky.graph.follow",
            "record": {
                "$type": "app.bsky.graph.follow",
                "subject": did,
                "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            },
        })
        return {
            "uri": res.get("uri") or "",
            "cid": res.get("cid") or "",
            "did": did,
            "handle": prof.get("handle") or actor,
        }

    def unfollow(self, actor: str) -> dict:
        actor = (actor or "").lstrip("@").strip()
        prof = self.get_profile(actor)
        existing = ((prof.get("viewer") or {}).get("following") or "") or ""
        if not existing:
            return {
                "skipped": "not following",
                "did": prof.get("did") or "",
                "handle": prof.get("handle") or actor,
            }
        rkey = uri_rkey(existing)
        self.post("com.atproto.repo.deleteRecord", {
            "repo": self.did,
            "collection": "app.bsky.graph.follow",
            "rkey": rkey,
        })
        return {
            "deleted": existing,
            "did": prof.get("did") or "",
            "handle": prof.get("handle") or actor,
        }

    def notifications(self, limit: int = 50, cursor: str | None = None, reasons: list[str] | None = None) -> dict:
        params = {"limit": str(min(max(limit, 1), 100))}
        if cursor:
            params["cursor"] = cursor
        if reasons:
            # Some PDS builds accept repeated reasons; pass comma-joined as fallback later if needed.
            params["reasons"] = reasons[0] if len(reasons) == 1 else None
        doc = self.get("app.bsky.notification.listNotifications", params)
        notes = doc.get("notifications") or []
        if reasons and len(reasons) > 1:
            notes = [n for n in notes if n.get("reason") in reasons]
            doc = dict(doc)
            doc["notifications"] = notes
        return doc

    def notifications_since(self, since: datetime, reasons: list[str] | None = None, max_pages: int = 10) -> list[dict]:
        if since.tzinfo is None:
            since = since.replace(tzinfo=timezone.utc)
        out = []
        cursor = None
        for _ in range(max_pages):
            doc = self.notifications(limit=100, cursor=cursor, reasons=None)
            batch = doc.get("notifications") or []
            if not batch:
                break
            stop = False
            for n in batch:
                ts = n.get("indexedAt") or n.get("record", {}).get("createdAt") or ""
                try:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                except ValueError:
                    dt = None
                if dt is not None and dt < since:
                    stop = True
                    continue
                if reasons and n.get("reason") not in reasons:
                    continue
                out.append(n)
            if stop:
                break
            cursor = doc.get("cursor")
            if not cursor:
                break
        return out


def summarize_profile(prof: dict) -> dict:
    return {
        "handle": prof.get("handle"),
        "did": prof.get("did"),
        "displayName": prof.get("displayName") or "",
        "description": (prof.get("description") or "")[:500],
        "followersCount": prof.get("followersCount"),
        "followsCount": prof.get("followsCount"),
        "postsCount": prof.get("postsCount"),
        "following": bool((prof.get("viewer") or {}).get("following")),
        "followedBy": bool((prof.get("viewer") or {}).get("followedBy")),
        "labels": [((lb.get("val") if isinstance(lb, dict) else lb) or "") for lb in (prof.get("labels") or [])],
    }


def summarize_post(post: dict) -> dict:
    author = post.get("author") or {}
    rec = post.get("record") or {}
    viewer = post.get("viewer") or {}
    uri = post.get("uri") or ""
    return {
        "uri": uri,
        "cid": post.get("cid") or "",
        "url": at_uri_url(uri, author.get("handle")),
        "author": author.get("handle") or "",
        "text": rec.get("text") or "",
        "likeCount": post.get("likeCount"),
        "replyCount": post.get("replyCount"),
        "viewerLike": bool(viewer.get("like")),
        "viewerReply": bool(viewer.get("reply")),
    }


def summarize_notification(n: dict) -> dict:
    author = n.get("author") or {}
    rec = n.get("record") or {}
    uri = n.get("uri") or ""
    return {
        "reason": n.get("reason"),
        "indexedAt": n.get("indexedAt"),
        "isRead": n.get("isRead"),
        "author": author.get("handle") or "",
        "authorDid": author.get("did") or "",
        "uri": uri,
        "url": at_uri_url(uri, author.get("handle")),
        "reasonSubject": n.get("reasonSubject") or "",
        "text": rec.get("text") or "",
    }


def looks_ai_or_spammy(prof: dict) -> str | None:
    """Return a skip reason if the account looks like an AI/bot or spam, else None."""
    handle = (prof.get("handle") or "").lower()
    name = (prof.get("displayName") or "").lower()
    bio = (prof.get("description") or "").lower()
    blob = " ".join([handle, name, bio])
    markers = [
        "ai agent", "ai-operated", "ai operated", "autonomous ai", "autonomous agent",
        "i am a bot", "i'm a bot", "this is a bot", "bot account",
        "run by an ai", "operated by an ai", "ai-run", "ai run account",
        "automated account", "llm agent", "self-described ai",
    ]
    for m in markers:
        if m in blob:
            return f"bio/name looks AI/bot ({m!r})"
    # Very new empty accounts with no posts and a spammy handle pattern.
    posts = prof.get("postsCount") or 0
    followers = prof.get("followersCount") or 0
    if posts == 0 and followers == 0 and not (prof.get("description") or "").strip():
        return "empty/spammy (0 posts, 0 followers, empty bio)"
    return None


def _print_json(obj) -> None:
    print(json.dumps(redact_obj(obj), indent=2, ensure_ascii=False))


def cmd_login(_args) -> int:
    c = credentials()
    log("login: " + creds_note(c))
    client = Client(c)
    info = client.login()
    _print_json(info)
    return 0


def cmd_profile(args) -> int:
    client = Client()
    client.login()
    prof = client.get_profile(args.handle)
    _print_json(summarize_profile(prof))
    return 0


def cmd_thread(args) -> int:
    client = Client()
    client.login()
    post = client.thread_post(args.url, depth=int(args.depth))
    existing = client.already_replied(args.url)
    info = summarize_post(post)
    info["alreadyReplied"] = bool(existing)
    if existing:
        info["ourReply"] = summarize_post(existing)
    _print_json(info)
    return 0


def cmd_reply(args) -> int:
    client = Client()
    client.login()
    res = client.reply(args.url, args.text, skip_if_replied=not args.force)
    _print_json(res)
    return 0


def cmd_like(args) -> int:
    client = Client()
    client.login()
    res = client.like(args.url, skip_if_liked=not args.force)
    _print_json(res)
    return 0


def cmd_follow(args) -> int:
    client = Client()
    client.login()
    if not args.force:
        prof = client.get_profile(args.handle)
        reason = looks_ai_or_spammy(prof)
        if reason:
            _print_json({
                "skipped": reason,
                "handle": prof.get("handle"),
                "did": prof.get("did"),
            })
            return 0
    res = client.follow(args.handle, skip_if_following=not args.force)
    _print_json(res)
    return 0


def cmd_unfollow(args) -> int:
    client = Client()
    client.login()
    res = client.unfollow(args.handle)
    _print_json(res)
    return 0


def cmd_notifications(args) -> int:
    client = Client()
    client.login()
    reasons = [r.strip() for r in (args.reasons or "").split(",") if r.strip()] or None
    if args.since:
        since = args.since.strip()
        if since.endswith("Z"):
            since = since[:-1] + "+00:00"
        dt = datetime.fromisoformat(since)
        notes = client.notifications_since(dt, reasons=reasons)
    else:
        notes = client.notifications(limit=args.limit or 50, reasons=reasons).get("notifications") or []
    _print_json([summarize_notification(n) for n in notes])
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("login", help="create a session and print handle/did only")
    p.set_defaults(func=cmd_login)

    p = sub.add_parser("profile", help="print a public profile summary")
    p.add_argument("handle")
    p.set_defaults(func=cmd_profile)

    p = sub.add_parser("thread", help="print a post summary and whether we already replied")
    p.add_argument("url")
    p.add_argument("--depth", default=3)
    p.set_defaults(func=cmd_thread)

    p = sub.add_parser("reply", help="reply to a post (skips if we already replied)")
    p.add_argument("url")
    p.add_argument("text")
    p.add_argument("--force", action="store_true", help="post even if we already replied")
    p.set_defaults(func=cmd_reply)

    p = sub.add_parser("like", help="like a post (skips if already liked)")
    p.add_argument("url")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_like)

    p = sub.add_parser("follow", help="follow a handle (skips if already following or AI/spammy)")
    p.add_argument("handle")
    p.add_argument("--force", action="store_true", help="follow even if already following / AI-or-spammy check")
    p.set_defaults(func=cmd_follow)

    p = sub.add_parser("unfollow", help="unfollow a handle (no-op if not following)")
    p.add_argument("handle")
    p.set_defaults(func=cmd_unfollow)

    p = sub.add_parser("notifications", help="list notifications (text only; no tokens)")
    p.add_argument("--since", help="ISO timestamp (inclusive); pages until older")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--reasons", help="comma-separated reasons (reply,mention,quote,...)")
    p.set_defaults(func=cmd_notifications)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except Exception as e:
        log(f"error: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
