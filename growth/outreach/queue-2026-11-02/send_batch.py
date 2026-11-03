#!/usr/bin/env python3
"""Nov 2 2026 cold-email sender: one at a time, 15-30 min jitter, ET window 8:30-19:00,
waits while growth/outreach/PAUSE-SENDS exists, stops on any SMTP error. Never prints secrets."""
import json, os, random, smtplib, ssl, sys, time, csv, io, fcntl, tempfile, traceback
from datetime import datetime, time as dtime
from zoneinfo import ZoneInfo
from email.message import EmailMessage
from email.utils import make_msgid, formatdate

ROOT = "/workspace/skillmaxx"
BATCH = f"{ROOT}/growth/outreach/queue-2026-11-02/batch.json"
RESULTS = f"{ROOT}/growth/outreach/sent/2026-11-02-email-results.json"
PIPE = f"{ROOT}/growth/sponsors/PIPELINE.csv"
PIPE_LOCK = f"{ROOT}/growth/sponsors/.PIPELINE.csv.lock"
PAUSE = f"{ROOT}/growth/outreach/PAUSE-SENDS"
ENV = "/home/box/.skillmaxx-secrets/accounts.env"
ET = ZoneInfo("America/New_York")
START, END = dtime(8, 30), dtime(19, 0)
DAY = "2026-11-02"

def now(): return datetime.now(ET)
def log(msg): print(f"[{now():%Y-%m-%d %H:%M:%S} ET] {msg}", flush=True)

def atomic_write(path, text):
    d = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".tmp-", text=True)
    with os.fdopen(fd, "w", newline="") as f: f.write(text)
    os.replace(tmp, path)

def load_results():
    try: return json.load(open(RESULTS))
    except FileNotFoundError: return []

def append_result(rec):
    r = load_results(); r.append(rec)
    atomic_write(RESULTS, json.dumps(r, indent=2, ensure_ascii=False) + "\n")

def update_pipeline(company, to, subject, t):
    with open(PIPE_LOCK, "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        raw = open(PIPE, newline="").read()   # re-read right before write
        rows = list(csv.DictReader(io.StringIO(raw)))
        fields = list(rows[0].keys())
        hit = 0
        for r in rows:
            if r["company"] == company and r["contact_detail"].strip().lower() == to.lower():
                r["status"] = "Contacted"; r["date_contacted"] = DAY
                r["outreach_sent"] = f'Cold email #1 from skillmaxx@gilventures.ai to {to} (subject "{subject}") at {t:%-I:%M %p} ET'
                r["next_follow_up"] = "2026-11-09, then 2026-11-16 (final)"
                hit += 1
        if hit != 1:
            log(f"WARN pipeline row match count for {company}/{to} = {hit}; CSV not changed"); return
        o = io.StringIO(); w = csv.DictWriter(o, fieldnames=fields, lineterminator="\r\n")
        w.writeheader(); w.writerows(rows)
        atomic_write(PIPE, o.getvalue())
        fcntl.flock(lk, fcntl.LOCK_UN)
    log(f"PIPELINE.csv updated: {company} -> Contacted")

def in_window(t): return START <= t.time() < END

def gate():
    """Return True if OK to send now, False if the batch must stop."""
    t = now()
    if t.date().isoformat() != DAY or not in_window(t):
        log(f"STOP: outside 8:30 AM-7:00 PM ET window on {DAY} (now {t:%Y-%m-%d %H:%M})"); return False
    if os.path.exists(PAUSE):
        log("PAUSE-SENDS present; waiting (polling every 60s)")
        while os.path.exists(PAUSE):
            time.sleep(60)
            t = now()
            if not in_window(t):
                log("STOP: PAUSE-SENDS still present at/after 7:00 PM ET"); return False
        log("PAUSE-SENDS removed; continuing")
        if not in_window(now()): log("STOP: outside window"); return False
    return True

def creds():
    env = {}
    for l in open(ENV):
        if "=" in l:
            k, v = l.rstrip("\n").split("=", 1); env[k.strip()] = v.strip().strip('"').strip("'")
    return env["zoho_admin_login"], env["zoho_admin_password"]

def send(e, user, pw):
    m = EmailMessage()
    m["From"] = "Brandon at SkillMaxx <skillmaxx@gilventures.ai>"
    m["To"] = e["to"]; m["Subject"] = e["subject"]
    m["Date"] = formatdate(localtime=True); m["Message-ID"] = make_msgid(domain="gilventures.ai")
    m.set_content(e["body"])
    with smtplib.SMTP_SSL("smtp.zoho.com", 465, context=ssl.create_default_context(), timeout=60) as s:
        s.login(user, pw)
        refused = s.send_message(m)
    if refused: raise smtplib.SMTPRecipientsRefused(refused)
    return m["Message-ID"]

def main():
    batch = json.load(open(BATCH))
    done = {(r["company"], r["to"]) for r in load_results() if r.get("status") == "sent"}
    todo = [e for e in batch if (e["company"], e["to"]) not in done]
    log(f"sender start pid={os.getpid()} todo={len(todo)} (already sent {len(done)})")
    user, pw = creds()
    for i, e in enumerate(todo):
        if i > 0:
            remaining = len(todo) - i
            left_min = (datetime.combine(now().date(), END, ET) - now()).total_seconds() / 60 - 5
            gap = random.uniform(15, 30)
            if remaining and left_min / remaining < gap:
                gap = max(15.0, min(gap, left_min / remaining)) + random.uniform(0, 1.5)
            log(f"next: {e['company']} in {gap:.1f} min")
            time.sleep(gap * 60)
        if not gate(): break
        t = now()
        rec = dict(company=e["company"], to=e["to"], source_url=e.get("source_url", ""), subject=e["subject"],
                   status="", error="", message_id="", sent_at_et="")
        try:
            mid = send(e, user, pw)
            t = now()
            rec.update(status="sent", message_id=mid, sent_at_et=f"{t:%Y-%m-%d %H:%M:%S} ET")
            append_result(rec)
            log(f"SENT {i+1}/{len(todo)} {e['company']} <{e['to']}> {mid}")
            try: update_pipeline(e["company"], e["to"], e["subject"], t)
            except Exception as pe: log(f"WARN pipeline update failed for {e['company']}: {pe!r}")
        except Exception as ex:
            rec.update(status="error", error=f"{type(ex).__name__}: {ex}"[:500], sent_at_et=f"{now():%Y-%m-%d %H:%M:%S} ET")
            append_result(rec)
            log(f"STOP: SMTP error on {e['company']} <{e['to']}>: {rec['error']}")
            break
    log("sender exit")

if __name__ == "__main__":
    try: main()
    except Exception: log("FATAL " + traceback.format_exc().replace("\n", " | ")[:1500])
