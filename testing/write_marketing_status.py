#!/usr/bin/env python3
"""Write ~/.local/share/skillmaxx/marketing-status.json for Brandon HQ auto-discovery.

Launch-kit schema v1 (grandpajackai/launch-kit integrations/brandon-hq/marketing.py
status_to_business): schema_version == 1, name, owner, light, headline (list),
kpis (dict), details, issues, needs, plus needs_brandon and updated_at.

Never writes under ~/.local/share/skillmaxx/work. Never prints secrets.
stdlib only. Failures are non-fatal when called as `python3 ... || true`.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/New_York")
SCHEMA_VERSION = 1
NAME = "SkillMaxx"
OWNER = "SkillMaxx CEO"
BUSINESS_KEY = "skillmaxx"
DEFAULT_OUT = Path.home() / ".local/share/skillmaxx/marketing-status.json"
WORK_DIR = Path.home() / ".local/share/skillmaxx/work"
BEEHIIV_ENV = Path.home() / ".skillmaxx-secrets" / "beehiiv.env"
CTA_NEED = "Pick the carousel CTA (currently the newsletter)"
REQUIRED_KEYS = (
    "name",
    "owner",
    "light",
    "headline",
    "kpis",
    "details",
    "issues",
    "needs",
    "needs_brandon",
    "updated_at",
)
TIMEOUT_SEC = 10

# Status tokens used only for counts. Never copy row notes (they may contain contacts).
SUBMITTED_TOKS = (
    "submitted",
    "emailed",
    "open",
    "contacted",
    "sent",
)
ACCEPTED_TOKS = (
    "accepted",
    "done",
    "live",
    "merged",
    "listed",
    "approved",
)
HEADER_TOKS = {"place", "status", "#", "url", "date", "category", "route / url", "link"}


def now_et() -> datetime:
    return datetime.now(TZ)


def iso_et(dt: datetime | None = None) -> str:
    return (dt or now_et()).isoformat(timespec="seconds")


def repo_root(explicit: Path | None = None) -> Path:
    if explicit:
        return explicit.resolve()
    return Path(__file__).resolve().parents[1]


def state_dir(explicit: Path | None = None) -> Path:
    if explicit:
        return explicit.expanduser().resolve()
    env = os.environ.get("SKILLMAXX_STATE")
    if env:
        return Path(env).expanduser()
    return Path.home() / ".local/share/skillmaxx"


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


def safe_json_load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def count_subscribers(timeout: int = TIMEOUT_SEC):
    """Return (value, note). value is int or 'unknown'. Never log the API key."""
    env_path = Path(os.environ.get("SKILLMAXX_BEEHIIV_ENV", str(BEEHIIV_ENV))).expanduser()
    vals = load_env_file(env_path)
    api_key = os.environ.get("BEEHIIV_API_KEY") or vals.get("BEEHIIV_API_KEY") or ""
    pub_id = os.environ.get("BEEHIIV_PUBLICATION_ID") or vals.get("BEEHIIV_PUBLICATION_ID") or ""
    if not api_key or not pub_id:
        return "unknown", "Beehiiv key or publication id not available on this host"
    try:
        q = urllib.parse.urlencode({"limit": 1, "page": 1})
        url = f"https://api.beehiiv.com/v2/publications/{pub_id}/subscriptions?{q}"
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
                "User-Agent": "skillmaxx-marketing-status/1.0",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = json.loads(r.read().decode("utf-8", "replace"))
        # Prefer aggregate totals so we never persist subscription records.
        total = body.get("total_results")
        if total is None:
            meta = body.get("meta") or {}
            total = meta.get("total_results") or meta.get("total")
        if total is None:
            return "unknown", "Beehiiv API returned no total_results"
        return int(total), "Beehiiv subscriptions total_results (includes any test accounts)"
    except Exception:
        return "unknown", "Beehiiv API request failed or timed out"


def count_posts(root: Path) -> tuple[int, int, str]:
    published_dir = root / "src" / "blog"
    queued_dir = root / "growth" / "content" / "queue"
    published = 0
    if published_dir.is_dir():
        for p in published_dir.iterdir():
            if p.suffix.lower() in {".njk", ".md"} and p.stem.lower() != "index":
                published += 1
    queued = 0
    if queued_dir.is_dir():
        for p in queued_dir.iterdir():
            if p.suffix.lower() in {".njk", ".md"} and p.stem.lower() != "readme":
                queued += 1
    label = f"{published} published blog posts, {queued} queued drafts (src/blog + growth/content/queue)"
    return published, queued, label


def _is_header_row(cells: list[str]) -> bool:
    labels = [re.sub(r"[*`]", "", c).strip().lower() for c in cells]
    return "status" in labels or any(c in HEADER_TOKS or c.startswith("place") for c in labels[:3])


def _status_index(header: list[str] | None) -> int | None:
    if not header:
        return None
    for i, c in enumerate(header):
        if re.sub(r"[*`]", "", c).strip().lower() == "status":
            return i
    return None


def _is_sep_row(line: str) -> bool:
    inner = line.strip().strip("|").replace("|", "")
    return bool(inner) and set(inner.strip()) <= set("-: ")


def count_listings(root: Path) -> tuple[int, int, str, dict[str, int]]:
    listings = root / "growth" / "listings"
    seen: set[str] = set()
    statuses: list[str] = []
    if listings.is_dir():
        for path in sorted(listings.glob("*.md")):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            header: list[str] | None = None
            status_i: int | None = None
            for line in text.splitlines():
                if not line.startswith("|") or _is_sep_row(line):
                    continue
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if not cells:
                    continue
                if _is_header_row(cells):
                    header = cells
                    status_i = _status_index(header)
                    continue
                # Dedupe on the place/name cell so LISTINGS + BROWSER-QUEUE don't double-count.
                place = cells[1] if cells and cells[0].isdigit() and len(cells) > 1 else cells[0]
                key = re.sub(r"\s+", " ", re.sub(r"[*`]", "", place)).strip().lower()
                if not key or key in seen:
                    continue
                seen.add(key)
                st = ""
                if status_i is not None and status_i < len(cells):
                    st = re.sub(r"\*+", "", cells[status_i]).strip()
                    if "http" in st.lower() or "@" in st:
                        st = ""
                statuses.append(st or "unknown")
    submitted = 0
    accepted = 0
    breakdown: Counter[str] = Counter()
    for st in statuses:
        key = re.sub(r"\s+", " ", st).strip()
        breakdown[key] += 1
        cl = key.lower()
        if any(tok in cl for tok in ACCEPTED_TOKS):
            accepted += 1
        elif any(tok in cl for tok in SUBMITTED_TOKS):
            submitted += 1
    note = (
        f"{submitted} submitted, {accepted} accepted "
        f"({len(statuses)} unique rows in growth/listings/*.md; counts only)"
    )
    return submitted, accepted, note, dict(breakdown)


def count_pipeline(root: Path) -> tuple[int | str, str, dict[str, int]]:
    path = root / "growth" / "sponsors" / "PIPELINE.csv"
    if not path.is_file():
        return "unknown", "PIPELINE.csv not found", {}
    try:
        with path.open(newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fields = reader.fieldnames or []
    except (OSError, csv.Error):
        return "unknown", "PIPELINE.csv could not be read", {}
    status_col = next((c for c in fields if c and "status" in c.lower()), None)
    breakdown: Counter[str] = Counter()
    n = 0
    for row in rows:
        if not any((v or "").strip() for v in row.values()):
            continue
        n += 1
        if status_col:
            st = (row.get(status_col) or "").strip() or "(empty)"
            # Status labels only — never company or contact columns.
            breakdown[st] += 1
    note = f"{n} rows in growth/sponsors/PIPELINE.csv (status counts only)"
    return n, note, dict(breakdown)


def last_successful_publish(root: Path, state: Path) -> tuple[str, str]:
    ps = state / "publish-status"
    if ps.is_file():
        try:
            raw = ps.read_text(encoding="utf-8", errors="replace").strip()
        except OSError:
            raw = ""
        parts = raw.split()
        if len(parts) >= 2 and parts[-1].lower() == "published":
            date = parts[0]
            try:
                mtime = datetime.fromtimestamp(ps.stat().st_mtime, TZ)
                return iso_et(mtime), f"Mac publish-status: {date} published"
            except OSError:
                return date, f"Mac publish-status: {date} published"
    reports = root / "src" / "_data" / "reports.json"
    doc = safe_json_load(reports)
    if isinstance(doc, list) and doc:
        best = None
        for row in doc:
            if not isinstance(row, dict):
                continue
            d = row.get("date") or ""
            if not d:
                continue
            if best is None or d > best[0]:
                best = (d, row.get("run_at") or d)
        if best:
            return str(best[1]), "latest date in src/_data/reports.json (repo fallback)"
    latest = safe_json_load(root / "src" / "_data" / "latestRows.json")
    if isinstance(latest, dict) and latest.get("date"):
        return str(latest["date"]), "src/_data/latestRows.json date (repo fallback)"
    return "unknown", "no publish-status or reports.json date found"


def pending_telegram_titles(root: Path) -> list[str]:
    path = root / "growth" / "telegram" / "REQUESTS.json"
    doc = safe_json_load(path)
    if not isinstance(doc, list):
        return []
    out: list[str] = []
    for item in doc:
        if not isinstance(item, dict):
            continue
        status = str(item.get("status") or item.get("state") or "pending").strip().lower()
        if status in {"done", "sent", "closed", "cancelled", "canceled", "complete"}:
            continue
        title = str(item.get("title") or "").strip()
        if not title or "@" in title:
            continue
        out.append(title)
    return out


def publish_outcome(state: Path) -> str:
    """Return published|failed|hold|unknown from $STATE/publish-status."""
    ps = state / "publish-status"
    if not ps.is_file():
        return "unknown"
    try:
        raw = ps.read_text(encoding="utf-8", errors="replace").strip().split()
    except OSError:
        return "unknown"
    if not raw:
        return "unknown"
    return raw[-1].lower()


def pick_light(outcome: str, unknown_sources: bool, needs_brandon: list[str]) -> str:
    if outcome == "failed":
        return "red"
    if unknown_sources or needs_brandon:
        return "yellow"
    return "green"


def headline_for(light: str, outcome: str, needs_brandon: list[str]) -> list[str]:
    if light == "red":
        return ["SkillMaxx nightly publish failed"]
    if outcome == "hold":
        return ["SkillMaxx publish held; report not updated"]
    if needs_brandon:
        return ["SkillMaxx marketing is running; items need Brandon"]
    return ["SkillMaxx marketing status is current"]


def refuse_work_path(dest: Path) -> None:
    resolved = dest.resolve()
    try:
        work = WORK_DIR.resolve()
    except OSError:
        work = WORK_DIR
    if resolved == work or work in resolved.parents:
        raise SystemExit("refusing to write under ~/.local/share/skillmaxx/work")


def atomic_write(dest: Path, doc: dict) -> None:
    refuse_work_path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".tmp")
    tmp.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, dest)
    try:
        dest.chmod(0o644)
    except OSError:
        pass


def build_status(root: Path, state: Path) -> dict:
    unknown: list[str] = []
    issues: list[str] = []
    details: list[str] = []

    subs, subs_note = count_subscribers()
    if subs == "unknown":
        unknown.append("subscribers")
    details.append(f"Subscribers: {subs} — {subs_note}")

    pub_n, queued_n, posts_note = count_posts(root)
    posts_value = f"{pub_n} published, {queued_n} queued"
    details.append(f"Posts published or queued: {posts_value} — {posts_note}")

    sub_n, acc_n, list_note, list_break = count_listings(root)
    list_value = f"{sub_n} submitted, {acc_n} accepted"
    details.append(f"Listings submitted or accepted: {list_value} — {list_note}")
    if list_break:
        # Counts only; keys are status labels from the tables, not contacts.
        parts = ", ".join(f"{k} {v}" for k, v in sorted(list_break.items(), key=lambda kv: (-kv[1], kv[0])))
        if "@" not in parts:
            details.append(f"Listings status counts: {parts}")

    pipe_n, pipe_note, pipe_break = count_pipeline(root)
    if pipe_n == "unknown":
        unknown.append("sponsor_pipeline")
    details.append(f"Sponsor pipeline: {pipe_n} — {pipe_note}")
    if pipe_break:
        parts = ", ".join(f"{k} {v}" for k, v in sorted(pipe_break.items(), key=lambda kv: (-kv[1], kv[0])))
        if "@" not in parts:
            details.append(f"Sponsor pipeline status counts: {parts}")

    last, last_note = last_successful_publish(root, state)
    if last == "unknown":
        unknown.append("last_successful_publish")
    details.append(f"Last successful publish: {last} — {last_note}")

    outcome = publish_outcome(state)
    if outcome == "failed":
        issues.append("Nightly publish failed (see Mac publish-status)")
    elif outcome == "hold":
        issues.append("Publish held by provenance checks; site shows the gap note")
    elif outcome == "unknown":
        details.append("Mac publish-status not present; light uses repo data only")

    needs_brandon = [CTA_NEED]
    needs_brandon.extend(pending_telegram_titles(root))

    light = pick_light(outcome, bool(unknown), needs_brandon)
    updated = iso_et()
    kpis = {
        "subscribers": subs,
        "posts_published_or_queued": posts_value,
        "listings_submitted_or_accepted": list_value,
        "sponsor_pipeline": pipe_n,
        "last_successful_publish": last,
    }
    doc = {
        "schema_version": SCHEMA_VERSION,
        "business_key": BUSINESS_KEY,
        "name": NAME,
        "owner": OWNER,
        "light": light,
        "headline": headline_for(light, outcome, needs_brandon),
        "kpis": kpis,
        "details": details,
        "issues": issues,
        "needs": list(needs_brandon),
        "needs_brandon": list(needs_brandon),
        "errors": [],
        "updated_at": updated,
        "generated_at": updated,
        "timezone": "America/New_York",
    }
    return doc


def validate(doc: dict) -> None:
    missing = [k for k in REQUIRED_KEYS if k not in doc]
    if missing:
        raise SystemExit(f"missing keys: {missing}")
    blob = json.dumps(doc, ensure_ascii=False)
    if "@" in blob:
        raise SystemExit("refusing to write status document that contains '@'")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Write SkillMaxx launch-kit marketing-status.json")
    p.add_argument("--out", type=Path, default=None, help="Output path (default: ~/.local/share/skillmaxx/marketing-status.json)")
    p.add_argument("--repo", type=Path, default=None, help="SkillMaxx repo root")
    p.add_argument("--state", type=Path, default=None, help="SKILLMAXX_STATE directory")
    args = p.parse_args(argv)
    root = repo_root(args.repo)
    state = state_dir(args.state)
    dest = (args.out or DEFAULT_OUT).expanduser()
    try:
        doc = build_status(root, state)
        validate(doc)
        atomic_write(dest, doc)
    except SystemExit:
        raise
    except Exception as exc:
        print(f"write_marketing_status: failed: {type(exc).__name__}", file=sys.stderr)
        return 1
    print(f"write_marketing_status: wrote {dest} light={doc['light']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
