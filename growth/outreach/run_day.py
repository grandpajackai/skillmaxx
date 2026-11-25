#!/usr/bin/env python3
"""Weekday sponsor-outreach sender. Refuses to send if the postal address is unset.

Usage (from the repo root or this directory):
  python3 growth/outreach/run_day.py --date 2026-11-25
  python3 growth/outreach/run_day.py --date 2026-11-25 --dry-run

Queue files (optional, all in growth/outreach/queue-YYYY-MM-DD/):
  jobs.json  — list of new pitches: [company, to, subject, name, why, source?]
  fu.json    — list of follow-ups: [company, to]
  plan.py    — may define NEW and FU in the same shapes if the JSON files are absent

Every send goes through zoho_mail.send(), which also holds while the postal
address is missing. Spacing is 20–60 minutes inside 9 AM–5 PM ET. The daily
cap is 20 if any bounce landed in the previous 7 days, otherwise the ramp cap
(max 30). Follow-ups are skipped when PIPELINE.csv is flagged bounced,
opted-out / do-not-contact, declined, or replied, and when the mailbox already
has a reply from that domain.
"""
from __future__ import annotations

import argparse, datetime as dt, fcntl, html, json, os, sys, time
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "growth" / "scripts"))

import lib
import outreach_config
import zoho_mail as z

ET = ZoneInfo("America/New_York")
LOCK_PATH = "/tmp/skillmaxx_outreach.lock"
PIPELINE = ROOT / "growth" / "sponsors" / "PIPELINE.csv"
PS = "P.S. If you'd like the weekly install results yourself, the SkillMaxx newsletter is free: https://skillmaxx.gilventures.ai/newsletter/"
BLOCK = ("kinde.com", "workos.com", "liveblocks.io")


def new_body(name, why, facts_line):
    return f"""Hi {name},

I'm Brandon. I run SkillMaxx, a free directory that install-tests agent skills, plugins and MCP servers nightly in Claude Code, Codex, Grok Build, Cursor and Pi (public logs: https://skillmaxx.gilventures.ai/reports/latest/). {facts_line}

{why}

Honest ask: would you take a founding Newsletter slot at $19/issue ($59/mo for 4)? Locked 6 months for the first 10 sponsors. Always labeled Sponsored; money never changes a test result.

We launched in Oct 2026, so the audience is small (hence the price). You'd get a monthly report with real numbers, even small ones.

A one-line "not now" helps too.

Brandon
SkillMaxx · https://skillmaxx.gilventures.ai/advertise/

{PS}
"""


def fu1_body():
    return f"""Hi again, one nudge, then I'll leave you alone.

Since my last note we published this week's install scorecard: https://skillmaxx.gilventures.ai/reports/week/2026-48/

If sponsoring isn't a fit, a one-line "not now" is genuinely helpful, and so is "test this instead".

Brandon

{PS}
"""


def latest_facts_line():
    reports = ROOT / "src" / "_data" / "reports.json"
    if reports.is_file():
        try:
            data = json.loads(reports.read_text())
            latest = data.get("latest") or data
            passed = latest.get("passed") or latest.get("pass")
            total = latest.get("total") or latest.get("judgeable") or latest.get("runs")
            if passed is not None and total is not None:
                return f"Last night {passed} of {total} installs passed."
        except Exception:
            pass
    return "Nightly results are public on the reports page."


def load_json(path: Path, default):
    return json.loads(path.read_text()) if path.is_file() else default


def load_queue(day: str):
    qdir = HERE / f"queue-{day}"
    jobs = load_json(qdir / "jobs.json", None)
    fus = load_json(qdir / "fu.json", None)
    if jobs is None or fus is None:
        sys.path.insert(0, str(qdir))
        try:
            import plan  # type: ignore
        except ImportError:
            plan = None
        if jobs is None:
            jobs = list(getattr(plan, "NEW", []) or [])
        if fus is None:
            fus = list(getattr(plan, "FU", []) or [])
    return qdir, jobs or [], fus or []


def addrs(m):
    return (m.get("toAddress") or "").lower()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", default=dt.datetime.now(ET).strftime("%Y-%m-%d"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ramp-cap", type=int, default=lib.RAMP_CAP)
    args = ap.parse_args()

    # Hold the batch before touching the lock or the mailbox.
    outreach_config.require_postal_address()

    qdir, new_jobs, fu_jobs = load_queue(args.date)
    res_path = HERE / "sent" / f"{args.date}-email-results.json"
    res = load_json(res_path, {"date": args.date, "sent": [], "skipped": [], "bounces": [], "stopped": None})

    def save():
        res_path.parent.mkdir(parents=True, exist_ok=True)
        res_path.write_text(json.dumps(res, indent=1) + "\n")

    if args.dry_run:
        rows = lib.load_pipeline(PIPELINE) if PIPELINE.is_file() else []
        today = dt.date.fromisoformat(args.date)
        cap = lib.daily_cap(today, lib.bounce_dates_from_pipeline(rows), args.ramp_cap)
        addr = outreach_config.postal_address()
        footer = lib.can_spam_footer(addr)
        print(f"DRY RUN date={args.date}")
        print(f"hold lifted: yes")
        print(f"postal address: {addr}")
        print("footer:")
        print(footer)
        print(f"daily cap: {cap}")
        print(f"spacing: {lib.MIN_GAP_SEC // 60}–{lib.MAX_GAP_SEC // 60} minutes ({lib.MIN_GAP_SEC}–{lib.MAX_GAP_SEC} seconds)")
        print(f"new jobs: {len(new_jobs)}")
        print(f"follow-ups: {len(fu_jobs)}")
        print("No email sent.")
        return

    lock = open(LOCK_PATH, "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        sys.exit("locked")

    rows = lib.load_pipeline(PIPELINE) if PIPELINE.is_file() else []
    today = dt.date.fromisoformat(args.date)
    cap = lib.daily_cap(today, lib.bounce_dates_from_pipeline(rows), args.ramp_cap)
    facts = latest_facts_line()
    done = {(r["company"], r["kind"]) for r in res["sent"]} | {(r["company"], r["kind"]) for r in res["skipped"]}

    def skip(c, k, why):
        res["skipped"].append({"company": c, "reason": why, "kind": k})
        done.add((c, k))
        save()
        print({"skipped": c, "kind": k, "reason": why}, flush=True)

    def nextjob():
        nn = sum(1 for r in res["sent"] if r.get("kind") == "new" and r.get("http") == 200)
        nf = sum(1 for r in res["sent"] if r.get("kind") == "fu1" and r.get("http") == 200)
        # Interleave 2 new, then 1 follow-up, honoring the daily cap.
        if nn + nf >= cap:
            return None
        want_fu = nn >= 2 * (nf + 1)
        if want_fu:
            for x in fu_jobs:
                if (x[0], "fu1") not in done:
                    return ("fu1", x)
        for x in new_jobs:
            if (x[0], "new") not in done:
                return ("new", x)
        for x in fu_jobs:
            if (x[0], "fu1") not in done:
                return ("fu1", x)
        return None

    while True:
        if not lib.in_send_window():
            res["stopped"] = "outside window"
            save()
            print("outside window")
            break
        sent_ok = sum(1 for r in res["sent"] if r.get("http") == 200)
        if sent_ok >= cap:
            res["stopped"] = f"daily cap {cap}"
            save()
            break
        job = nextjob()
        if not job:
            res["stopped"] = "queue empty"
            save()
            break
        kind, x = job
        company, to = x[0], x[1]
        dom = to.split("@", 1)[1]

        # Scan recent inbox for opt-outs from this domain and mark PIPELINE.
        if PIPELINE.is_file():
            row = lib.pipeline_row_for(rows, company, to)
            if kind == "fu1":
                reason = lib.should_skip_followup(row)
                if reason:
                    skip(company, kind, reason)
                    continue

        if any(dom.endswith(b) for b in BLOCK):
            skip(company, kind, "blocklisted inbound thread")
            continue

        S = z.list_folder("Sent", 400)
        mine = [m for m in S if dom in addrs(m)]
        inbox = z.list_folder("Inbox", 300) + z.list_folder("Spam", 100)
        others = [
            m for m in inbox
            if dom in (m.get("fromAddress") or "").lower()
            and "mailer-daemon" not in (m.get("fromAddress") or "").lower()
            and "postmaster" not in (m.get("fromAddress") or "").lower()
        ]
        # Opt-out language in a reply from this domain.
        for m in others:
            body = ""
            try:
                body = z.content(m["folderId"], m["messageId"])
            except Exception:
                body = m.get("subject") or ""
            if lib.is_opt_out_text((m.get("subject") or "") + "\n" + body):
                if PIPELINE.is_file():
                    row = lib.pipeline_row_for(rows, company, to)
                    if row:
                        new_row = lib.mark_opted_out(row)
                        for i, r in enumerate(rows):
                            if r is row or (
                                r.get("company") == row.get("company")
                                and r.get("contact_detail") == row.get("contact_detail")
                            ):
                                rows[i] = new_row
                                break
                        lib.write_pipeline(PIPELINE, rows, list(rows[0].keys()))
                skip(company, kind, "opt-out / do-not-contact reply")
                break
        else:
            others = [m for m in others if not lib.is_opt_out_text(m.get("subject") or "")]
            if others and not (kind == "new" and all("mailer" in (m.get("fromAddress") or "") for m in others)):
                skip(company, kind, "inbound from domain")
                continue
            if kind == "new":
                if mine:
                    skip(company, kind, "already in Sent")
                    continue
                subj = x[2]
                body = lib.append_footer(new_body(x[3], x[4], facts))
                st, jr = z.send(to, subj, body)
            else:
                if len(mine) < 1:
                    skip(company, kind, f"{len(mine)} in Sent, expected >=1")
                    continue
                m = mine[0]
                age = (time.time() * 1000 - int(m["receivedTime"])) / 86400000
                if age < 7:
                    skip(company, kind, "too recent")
                    continue
                subj = html.unescape(m["subject"])
                subj = subj if subj.lower().startswith("re:") else "Re: " + subj
                body = lib.append_footer(fu1_body())
                st, jr = z.send(to, subj, body, reply_to_mid=m["messageId"])
            rec = {
                "company": company,
                "to": to,
                "subject": subj,
                "kind": kind,
                "http": st,
                "zoho_messageId": jr.get("data", {}).get("messageId", ""),
                "sent_at": lib.now_et().strftime("%Y-%m-%d %H:%M:%S ET"),
                "via": "Zoho Mail API",
            }
            res["sent"].append(rec)
            done.add((company, kind))
            save()
            print(rec, flush=True)
            if st == 429 or st >= 500:
                res["stopped"] = f"HTTP {st}"
                save()
                break
            time.sleep(lib.sleep_seconds())
            continue
        # opted-out branch already skipped
        continue

    res["done"] = lib.now_et().isoformat()
    save()
    print("DONE")


if __name__ == "__main__":
    main()
