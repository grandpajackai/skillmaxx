#!/usr/bin/env python3
"""Alert once via Brandon HQ (Telegram + macOS) when SkillMaxx gets its first real Beehiiv subscriber.

Free, stdlib only, never prints secrets. Designed to run during the Mac nightly (or standalone).
Reads subscriber list from:
  1) --snapshot-file / $SKILLMAXX_STATE/beehiiv-subscribers.json (if present), OR
  2) Beehiiv API v2 using BEEHIIV_API_KEY (from env or ~/.skillmaxx-secrets/beehiiv.env).
If neither source is available, exits 0 quietly so the nightly never fails.

Excludes the 5 current Brandon test addresses (stored as SHA-256 hashes in
testing/beehiiv_test_subscribers.json, plus optional plaintext list in
$SKILLMAXX_STATE/test-subscribers.json or growth/newsletter/test-subscribers.local.json).

Fires ONCE only: writes $SKILLMAXX_STATE/first-subscriber-alerted.json after alert.py succeeds.
Usage: python3 testing/check_first_subscriber.py [--snapshot-file PATH] [--state-file PATH] [--hq-dir DIR] [--dry-run]"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PUB_ID = "pub_5c2d14be-2fac-4704-9dcd-b3d21a0e8a9c"
HASH_CFG = ROOT / "testing" / "beehiiv_test_subscribers.json"


def norm_email(email: str) -> str:
    return (email or "").strip().lower()


def sha256_email(email: str) -> str:
    return hashlib.sha256(norm_email(email).encode("utf-8")).hexdigest()


def load_env_file(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    except OSError:
        return {}
    return out


def load_excluded_hashes(state_dir: Path, extra_paths: list[Path] | None = None) -> set[str]:
    hashes: set[str] = set()
    if HASH_CFG.is_file():
        try:
            doc = json.loads(HASH_CFG.read_text(encoding="utf-8"))
            for h in doc.get("excluded_sha256") or []:
                if isinstance(h, str) and len(h) == 64:
                    hashes.add(h.lower())
        except Exception:
            pass
    candidates = [
        state_dir / "test-subscribers.json",
        ROOT / "growth" / "newsletter" / "test-subscribers.local.json",
        *(extra_paths or []),
    ]
    for p in candidates:
        if not p.is_file():
            continue
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
            items = doc if isinstance(doc, list) else (doc.get("emails") or doc.get("excluded") or [])
            for e in items:
                if isinstance(e, str) and "@" in e:
                    hashes.add(sha256_email(e))
        except Exception:
            pass
    return hashes


def load_from_snapshot(path: Path) -> list[dict] | None:
    if not path.is_file():
        return None
    doc = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(doc, list):
        return doc
    if isinstance(doc, dict):
        return doc.get("subscriptions") or doc.get("data") or []
    return None


def fetch_beehiiv_subscriptions(api_key: str, pub_id: str) -> list[dict]:
    all_subs: list[dict] = []
    page = 1
    while True:
        q = urllib.parse.urlencode({"limit": 100, "page": page})
        url = f"https://api.beehiiv.com/v2/publications/{pub_id}/subscriptions?{q}"
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
                "User-Agent": "skillmaxx-subscriber-check/1.0",
            },
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            body = json.loads(r.read().decode("utf-8", "replace"))
        rows = body.get("data") or []
        all_subs.extend(rows)
        total_pages = int(body.get("total_pages") or 1)
        if page >= total_pages or not rows:
            break
        page += 1
    return all_subs


def real_subscribers(subs: list[dict], excluded_hashes: set[str]) -> list[dict]:
    real: list[dict] = []
    for s in subs:
        status = str(s.get("status") or "active").lower()
        if status in ("inactive", "unsubscribed", "invalid"):
            continue
        email = norm_email(s.get("email") or "")
        if not email or "@" not in email:
            continue
        if sha256_email(email) in excluded_hashes:
            continue
        real.append({
            "id": s.get("id"),
            "status": status,
            "subscribed_on": s.get("subscribed_on") or s.get("created"),
            "acquisition_source": s.get("acquisition_source") or s.get("utm_source"),
            "email_sha256": sha256_email(email)[:12],
        })
    return real


def send_hq_alert(hq_dir: Path, real: list[dict]) -> tuple[bool, str]:
    if not (hq_dir / "hq" / "alert.py").is_file():
        return False, f"hq/alert.py not found under {hq_dir}"
    n = len(real)
    first = real[0]
    src = first.get("acquisition_source") or "direct"
    msg = (
        f"SkillMaxx Weekly got its first real (non-test) subscriber ({n} real, 5 test excluded). "
        f"Source: {src}. Time to review Beehiiv & un-hold Sunday issue email sends."
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = str(hq_dir) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    cmd = [
        sys.executable,
        "-m",
        "hq.alert",
        "--key",
        "skillmaxx_first_subscriber",
        "--severity",
        "info",
        "--title",
        "SkillMaxx: first real subscriber!",
        "--message",
        msg,
    ]
    r = subprocess.run(cmd, cwd=str(hq_dir), env=env, capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        return False, (r.stderr or r.stdout or f"exit {r.returncode}").strip()
    return True, r.stdout.strip()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot-file")
    ap.add_argument("--state-file")
    ap.add_argument("--hq-dir", default=os.path.expanduser("~/Projects/brandon-hq"))
    ap.add_argument("--pub-id", default=DEFAULT_PUB_ID)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    state_dir = Path(os.environ.get("SKILLMAXX_STATE", os.path.expanduser("~/.local/share/skillmaxx")))
    state_file = Path(a.state_file) if a.state_file else (state_dir / "first-subscriber-alerted.json")
    if state_file.is_file():
        print(f"subscriber-check: already alerted ({state_file}); skipping")
        return 0

    snap_path = Path(a.snapshot_file) if a.snapshot_file else (state_dir / "beehiiv-subscribers.json")
    subs: list[dict] | None = None
    source = ""
    if snap_path.is_file():
        try:
            subs = load_from_snapshot(snap_path)
            source = f"snapshot:{snap_path.name}"
        except Exception as e:
            print(f"subscriber-check: could not read snapshot ({type(e).__name__}); skipping")
            return 0
    else:
        env_path = Path(os.environ.get("SKILLMAXX_BEEHIIV_ENV", os.path.expanduser("~/.skillmaxx-secrets/beehiiv.env")))
        env_vals = load_env_file(env_path)
        api_key = os.environ.get("BEEHIIV_API_KEY") or env_vals.get("BEEHIIV_API_KEY") or ""
        pub_id = env_vals.get("BEEHIIV_PUBLICATION_ID") or a.pub_id
        if not api_key:
            print("subscriber-check: no BEEHIIV_API_KEY or snapshot file configured; skipping")
            return 0
        try:
            subs = fetch_beehiiv_subscriptions(api_key, pub_id)
            source = "beehiiv_api"
        except Exception as e:
            print(f"subscriber-check: Beehiiv API check failed ({type(e).__name__}); skipping")
            return 0

    excluded = load_excluded_hashes(state_dir)
    real = real_subscribers(subs or [], excluded)
    if not real:
        print(f"subscriber-check: 0 real subscribers ({len(subs or [])} total, test accounts excluded; {source})")
        return 0

    if a.dry_run:
        print(f"subscriber-check: DRY RUN would alert for {len(real)} real subscriber(s) ({source})")
        return 0

    ok, detail = send_hq_alert(Path(a.hq_dir), real)
    if not ok:
        print(f"subscriber-check: alert failed ({detail}); will retry next run")
        return 0

    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(
        json.dumps(
            {
                "alerted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "real_count": len(real),
                "source": source,
                "first_hash_prefix": real[0]["email_sha256"],
                "alert_result": detail,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"subscriber-check: alerted for {len(real)} real subscriber(s) ({detail})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
