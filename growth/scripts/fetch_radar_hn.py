#!/usr/bin/env python3
"""Fetch fresh Hacker News stories for SkillMaxx Weekly's Sunday "On our radar" section.

Keyless, free, stdlib only (hn.algolia.com). Runs at Sunday publish time in testing/publish_nightly.sh.
Never fails the nightly: on network errors or empty results it writes [] and exits 0.
Usage: python3 growth/scripts/fetch_radar_hn.py [--date YYYY-MM-DD] [--days 6] [--out PATH] [--limit 4]"""
import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, time, timedelta, timezone

UA = "skillmaxx-newsletter-radar/1.0 (+https://skillmaxx.gilventures.ai)"
QUERIES = ["mcp server", "claude code", "agent skills", "codex cli", "cursor mcp"]
TECH = re.compile(
    r"\b(mcp|model context protocol|claude|codex|cursor|grok|agent|skills?|plugins?|coding|cli|llm)\b",
    re.I,
)


def fetch_hn(query: str, start_ts: int, end_ts: int, hits: int = 8) -> list[dict]:
    q = urllib.parse.urlencode({
        "query": query,
        "tags": "story",
        "numericFilters": f"created_at_i>{start_ts},created_at_i<={end_ts}",
        "hitsPerPage": hits,
    })
    req = urllib.request.Request(
        f"https://hn.algolia.com/api/v1/search?{q}",
        headers={"User-Agent": UA, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=12) as r:
        data = json.loads(r.read().decode("utf-8", "replace"))
    return data.get("hits") or []


def gather(day: date, days: int = 6, limit: int = 4, min_points: int = 5) -> list[dict]:
    end_dt = datetime.combine(day, time(23, 59, 59), tzinfo=timezone.utc)
    now_dt = datetime.now(timezone.utc)
    if end_dt > now_dt:
        end_dt = now_dt
    start_ts = int((end_dt - timedelta(days=days)).timestamp())
    end_ts = int(end_dt.timestamp())
    seen: set[str] = set()
    items: list[dict] = []
    for q in QUERIES:
        try:
            hits = fetch_hn(q, start_ts, end_ts)
        except Exception:
            continue
        for h in hits:
            oid = str(h.get("objectID") or "").strip()
            title = (h.get("title") or "").strip()
            pts = int(h.get("points") or 0)
            if not oid or not title or oid in seen or pts < min_points:
                continue
            if not TECH.search(title):
                continue
            seen.add(oid)
            hn_url = f"https://news.ycombinator.com/item?id={oid}"
            ext_url = (h.get("url") or "").strip() or hn_url
            items.append({
                "title": title,
                "url": ext_url,
                "hn": hn_url,
                "points": pts,
                "comments": int(h.get("num_comments") or 0),
                "created": h.get("created_at") or "",
            })
    items.sort(key=lambda x: (-x["points"], -x["comments"]))
    return items[:limit]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--days", type=int, default=6)
    ap.add_argument("--limit", type=int, default=4)
    ap.add_argument("--min-points", type=int, default=5)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    try:
        d = date.fromisoformat(a.date)
        items = gather(d, days=a.days, limit=a.limit, min_points=a.min_points)
    except Exception:
        items = []
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=1)
    print(f"radar: wrote {len(items)} item(s) to {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
