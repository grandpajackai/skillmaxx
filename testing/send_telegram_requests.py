#!/usr/bin/env python3
"""Deliver queued SkillMaxx requests to Brandon via ~/Projects/brandon-hq (python3 -m hq.alert).

Reads growth/telegram/REQUESTS.json (list of {id, message, created, [title], [severity]})
and sends each unsent request once, recording sent IDs in
$SKILLMAXX_STATE/telegram-requests-sent.json.

Defaults severity to "critical" so 2 AM ET Mac nightly runs actually deliver to
Telegram instead of being deferred by hq.alert's 9 PM - 8 AM ET quiet hours.
Only marks an ID sent when hq.alert reports Telegram delivery succeeded.
Stdlib only; never prints secrets; exits 0 on missing HQ dir so nightly never breaks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REQUESTS = ROOT / "growth" / "telegram" / "REQUESTS.json"


def load_requests(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    doc = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(doc, dict):
        items = doc.get("requests") or []
    elif isinstance(doc, list):
        items = doc
    else:
        return []
    out: list[dict] = []
    for it in items:
        if not isinstance(it, dict):
            continue
        rid = str(it.get("id") or "").strip()
        msg = str(it.get("message") or "").strip()
        if rid and msg:
            out.append(it)
    return out


def load_sent(path: Path) -> dict:
    if not path.is_file():
        return {"sent": {}}
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(doc, dict) and isinstance(doc.get("sent"), dict):
            return doc
    except Exception:
        pass
    return {"sent": {}}


def save_sent(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def send_via_hq(hq_dir: Path, req: dict) -> tuple[bool, str, dict]:
    if not (hq_dir / "hq" / "alert.py").is_file():
        return False, f"hq/alert.py not found under {hq_dir}", {}
    rid = str(req["id"]).strip()
    sev = str(req.get("severity") or "critical").strip().lower()
    if sev not in ("info", "warn", "critical"):
        sev = "critical"
    title = str(req.get("title") or "SkillMaxx request").strip()
    msg = str(req["message"]).strip()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(hq_dir) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    cmd = [
        sys.executable,
        "-m",
        "hq.alert",
        "--key",
        f"skillmaxx_req_{rid}",
        "--severity",
        sev,
        "--title",
        title,
        "--message",
        msg,
    ]
    r = subprocess.run(cmd, cwd=str(hq_dir), env=env, capture_output=True, text=True, timeout=30)
    out = (r.stdout or "").strip()
    err = (r.stderr or "").strip()
    if r.returncode != 0:
        return False, err or out or f"exit {r.returncode}", {}
    parsed: dict = {}
    try:
        parsed = json.loads(out.splitlines()[-1]) if out else {}
    except Exception:
        parsed = {}
    if isinstance(parsed, dict) and parsed:
        chans = parsed.get("channels") or []
        ok = bool(parsed.get("ping")) and ("telegram" in chans)
        return ok, out, parsed
    ok = "telegram" in out.lower()
    return ok, out, parsed


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--requests-file", default=str(DEFAULT_REQUESTS))
    ap.add_argument("--state-file")
    ap.add_argument("--hq-dir", default=os.path.expanduser("~/Projects/brandon-hq"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    state_dir = Path(os.environ.get("SKILLMAXX_STATE", os.path.expanduser("~/.local/share/skillmaxx")))
    state_file = Path(a.state_file) if a.state_file else (state_dir / "telegram-requests-sent.json")
    reqs = load_requests(Path(a.requests_file))
    if not reqs:
        print("telegram-requests: no queued requests")
        return 0

    state = load_sent(state_file)
    sent_map = state.setdefault("sent", {})
    pending = [r for r in reqs if r["id"] not in sent_map]
    if not pending:
        print(f"telegram-requests: all {len(reqs)} request(s) already sent")
        return 0

    hq_dir = Path(a.hq_dir)
    if a.dry_run:
        for r in pending:
            print(f"telegram-requests: DRY RUN would send {r['id']}: {r['message'][:80]}")
        return 0

    if not (hq_dir / "hq" / "alert.py").is_file():
        print(f"telegram-requests: hq/alert.py not found under {hq_dir}; skipping ({len(pending)} pending)")
        return 0

    sent_now = 0
    for r in pending:
        rid = r["id"]
        ok, detail, parsed = send_via_hq(hq_dir, r)
        if not ok:
            print(f"telegram-requests: {rid} not delivered via Telegram ({detail}); will retry next run")
            continue
        sent_map[rid] = {
            "sent_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "created": r.get("created"),
            "title": r.get("title") or "SkillMaxx request",
            "message_sha256": hashlib.sha256(r["message"].encode("utf-8")).hexdigest()[:12],
            "channels": parsed.get("channels") if isinstance(parsed, dict) else None,
        }
        save_sent(state_file, state)
        sent_now += 1
        print(f"telegram-requests: sent {rid} ({detail})")

    print(f"telegram-requests: done ({sent_now} sent, {len(pending) - sent_now} still pending)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
