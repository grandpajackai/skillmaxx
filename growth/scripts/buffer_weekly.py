#!/usr/bin/env python3
"""Weekly social top-up without Grok or an LLM: 3 templated posts (Mon/Wed/Fri of next week)
built only from the latest weekly scorecard (src/_data/weeks.json).

Slots (ET): X 9:30 AM, LinkedIn 12:00 PM, Bluesky 7:30 PM.

X and LinkedIn stay on the Grok Buffer connector — this script does not call the
Buffer API for any channel (that path would create duplicates).

Bluesky is posted by growth/social/bluesky_post.py, not Buffer. This script enqueues
the three Bluesky texts into growth/social/bluesky-queue.json (--repo-queue) and/or
~/.local/share/skillmaxx/bluesky-queue.local.json (the default, so a Mac Sunday
publish can queue without another PR). Dedupes by text and by id.

Usage: python3 growth/scripts/buffer_weekly.py [--dry-run] [--week-of YYYY-MM-DD]
                                                [--repo-queue] [--local-queue]
"""
import json, os, sys, tempfile
from datetime import date, timedelta
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SITE = "https://skillmaxx.gilventures.ai"
REPO_QUEUE = os.path.join(ROOT, "growth", "social", "bluesky-queue.json")
LOCAL_QUEUE = os.path.expanduser("~/.local/share/skillmaxx/bluesky-queue.local.json")
CH = {"x": ("6adfb5c92f1f5ed648deaa83", 9, 30, 280), "linkedin": ("6adfc4f12f1f5ed648df8e37", 12, 0, 1400),
      "bluesky": ("6adfbe402f1f5ed648def519", 19, 30, 300)}
DAYS = ("mon", "wed", "fri")


def et_offset(d):  # US Eastern: EDT 2nd Sun Mar .. 1st Sun Nov
    y = d.year
    mar = date(y, 3, 8) + timedelta((6 - date(y, 3, 8).weekday()) % 7)
    nov = date(y, 11, 1) + timedelta((6 - date(y, 11, 1).weekday()) % 7)
    return "-04:00" if mar <= d < nov else "-05:00"


def posts(w):
    t = w["trend"][-1]; p, n = t["pass"], t["tested"]; rate = round(100 * p / n, 1) if n else 0
    rk = w["ranking"]; top = rk[0] if rk else None
    wk = f"{SITE}/reports/week/{w['key']}/"
    a = (f"Last week we ran real installs of agent skills, plugins and MCP servers in 5 coding agents. "
         f"Latest night: {p:,} of {n:,} passed ({rate}%). {w.get('fixed_n', 0)} fixed, {w.get('broke_n', 0)} broke. Scorecard: {wk}")
    by = ", ".join(f"{r['name']} {r['rate']}%" for r in rk)
    b = (f"Install pass rate by agent last week: {by}. Each agent gets the add-ons it supports, so it's add-on readiness, "
         f"not an agent ranking. {SITE}/works-in/")
    c = (f"{w.get('flaky_n', 0)} agent add-ons passed some nights and failed others last week. One bad install isn't "
         f"proof it's broken. Check the night-by-night history before you give up on one: {SITE}/reports/")
    return [a, b, c]


def load_queue(path):
    if not os.path.exists(path):
        return {"schema_version": 1, "items": []}
    try:
        doc = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return {"schema_version": 1, "items": []}
    if isinstance(doc, list):
        return {"schema_version": 1, "items": doc}
    if not isinstance(doc, dict):
        return {"schema_version": 1, "items": []}
    items = doc.get("items") or []
    if not isinstance(items, list):
        items = []
    doc["schema_version"] = doc.get("schema_version") or 1
    doc["items"] = items
    return doc


def atomic_write(path, doc):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".tmp-", dir=os.path.dirname(path) or ".")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def all_known_items():
    """Dedupe against both queue files so a local enqueue will not collide with a repo slot."""
    items = []
    for path in (REPO_QUEUE, LOCAL_QUEUE):
        items.extend(it for it in load_queue(path)["items"] if isinstance(it, dict))
    return items


def enqueue(path, new_items, dry):
    doc = load_queue(path)
    known = all_known_items()
    have_text = {(it.get("text") or "").strip() for it in known}
    have_id = {str(it.get("id") or "") for it in known}
    have_due = {str(it.get("due_at") or "") for it in known if it.get("due_at")}
    added = 0
    for it in new_items:
        if it["id"] in have_id or it["text"].strip() in have_text:
            print(f"bluesky {it['due_at']}: already queued, skip")
            continue
        if it["due_at"] in have_due:
            print(f"bluesky {it['due_at']}: slot already filled, skip")
            continue
        if dry:
            print(f"[plan] bluesky {it['due_at']} -> {path}: {it['text'][:120]}…")
            added += 1
            continue
        doc["items"].append(it)
        have_text.add(it["text"].strip())
        have_id.add(it["id"])
        have_due.add(it["due_at"])
        added += 1
        print(f"bluesky {it['due_at']}: enqueued {it['id']} -> {path}")
    if not dry and added:
        # keep due_at order
        def key(it):
            return it.get("due_at") or ""
        doc["items"] = sorted([x for x in doc["items"] if isinstance(x, dict)], key=key)
        atomic_write(path, doc)
    return added


def planned_bluesky(w, mon):
    texts = posts(w)
    out = []
    for i, txt in enumerate(texts):
        d = mon + timedelta(2 * i)  # Mon, Wed, Fri
        _, hh, mm, lim = CH["bluesky"]
        if len(txt) > lim:
            txt = txt[:lim - 1] + "…"
        due = f"{d.isoformat()}T{hh:02d}:{mm:02d}:00{et_offset(d)}"
        out.append({
            "id": f"weekly-{w.get('key', mon.isoformat())}-{DAYS[i]}",
            "text": txt,
            "due_at": due,
            "images": [],
            "source": "buffer_weekly",
            "week": w.get("key"),
        })
    return out


def main(argv):
    dry = "--dry-run" in argv
    # Default: write the local overlay (safe on the Mac after a publish).
    # --repo-queue also (or only, if --repo-queue is set without local) writes the in-repo file.
    write_local = "--local-queue" in argv or "--repo-queue" not in argv
    write_repo = "--repo-queue" in argv
    if "--repo-queue" not in argv and "--local-queue" not in argv:
        write_local = True
    weeks_path = os.path.join(ROOT, "src/_data/weeks.json")
    weeks = sorted(json.load(open(weeks_path)), key=lambda x: x["end"], reverse=True)
    w = next((x for x in weeks if x.get("runs")), None)
    if not w:
        print("no week with runs")
        return 0
    today = date.today()
    mon = date.fromisoformat(argv[argv.index("--week-of") + 1]) if "--week-of" in argv else today + timedelta(7 - today.weekday())
    items = planned_bluesky(w, mon)
    print("buffer_weekly: X and LinkedIn left to the Grok Buffer connector (no Buffer API calls)")
    print(f"buffer_weekly: {len(items)} Bluesky post(s) for week starting {mon.isoformat()} (scorecard {w.get('key')})")
    added = 0
    if write_local:
        added += enqueue(LOCAL_QUEUE, items, dry)
    if write_repo:
        added += enqueue(REPO_QUEUE, items, dry)
    if not write_local and not write_repo:
        for it in items:
            print(f"[plan] bluesky {it['due_at']}: {it['text']}")
    print(f"buffer_weekly: {added} Bluesky item(s) {'planned' if dry else 'enqueued'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
