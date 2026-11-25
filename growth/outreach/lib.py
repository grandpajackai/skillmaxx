"""Shared SkillMaxx sponsor-outreach helpers (CAN-SPAM, pacing, pipeline gates).

This module never sends email. Callers must go through zoho_mail.send(), which
also refuses to send while SKILLMAXX_POSTAL_ADDRESS is unset.
"""
from __future__ import annotations

import csv
import datetime as dt
import random
import re
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

from outreach_config import postal_address

ET = ZoneInfo("America/New_York")
WINDOW_START_HOUR = 9
WINDOW_END_HOUR = 17  # exclusive; 9 AM–5 PM ET
MIN_GAP_SEC = 20 * 60
MAX_GAP_SEC = 60 * 60
RAMP_CAP = 30
BOUNCE_CAP = 20
BOUNCE_LOOKBACK_DAYS = 7

OPT_OUT_RE = re.compile(
    r"\b("
    r"no thanks|no thank you|unsubscribe|opt[\s-]?out|"
    r"stop emailing|do not (?:email|contact)|don't (?:email|contact)|"
    r"remove me|take me off|please stop"
    r")\b",
    re.I,
)

# Statuses that mean a follow-up must not go out.
SKIP_FOLLOWUP_STATUSES = frozenset({
    "bounced",
    "do-not-contact",
    "do not contact",
    "opted-out",
    "opted out",
    "declined",
    "declined-warm",
    "replied",
    "lost",
    "warm - inbound",
    "booked",
    "live",
    "renewed",
})

GENERIC_LOCAL = frozenset({
    "hello", "hi", "hey", "info", "sales", "contact", "team", "support",
    "mail", "admin", "office", "help", "enquiries", "inquiries", "ask",
    "feedback", "press",
})
PREFERRED_LOCAL = frozenset({
    "partnerships", "partnership", "partners", "sponsors", "sponsor",
    "sponsorships", "sponsorship", "advertising", "advertise", "ads",
    "media", "bizdev", "bd", "collaborations", "collaboration",
})

FOOTER_OPT_OUT = 'Not interested? Reply "no thanks" and I won\'t email again.'

OUR_FROM_NEEDLES = (
    "skillmaxx@gilventures.ai",
    "brandon at skillmaxx",
    "brandon gil",
)


def now_et() -> dt.datetime:
    return dt.datetime.now(ET)


def in_send_window(when: dt.datetime | None = None) -> bool:
    n = when or now_et()
    return n.weekday() < 5 and WINDOW_START_HOUR <= n.hour < WINDOW_END_HOUR


def sleep_seconds() -> int:
    """Randomized 20–60 minute gap between sends."""
    return random.randint(MIN_GAP_SEC, MAX_GAP_SEC)


def can_spam_footer(address: str | None = None) -> str:
    addr = (address if address is not None else postal_address()).strip()
    if not addr:
        raise SystemExit(
            "Refusing to build a commercial email: SKILLMAXX_POSTAL_ADDRESS is unset."
        )
    return f"{FOOTER_OPT_OUT}\n{addr}"


def append_footer(body: str, address: str | None = None) -> str:
    footer = can_spam_footer(address)
    text = body.rstrip()
    if FOOTER_OPT_OUT.lower() in text.lower():
        return text + "\n"
    return f"{text}\n\n{footer}\n"


def bounce_dates_from_pipeline(rows: Iterable[dict]) -> list[dt.date]:
    dates: list[dt.date] = []
    for row in rows:
        if (row.get("status") or "").strip().lower() != "bounced":
            continue
        raw = (row.get("date_contacted") or "").strip()
        if re.match(r"\d{4}-\d{2}-\d{2}$", raw):
            dates.append(dt.date.fromisoformat(raw))
    return dates


def daily_cap(today: dt.date, bounce_dates: Iterable[dt.date], ramp_cap: int = RAMP_CAP) -> int:
    """20/day if any bounce landed in the previous 7 days; otherwise the ramp cap."""
    lookback_start = today - dt.timedelta(days=BOUNCE_LOOKBACK_DAYS)
    if any(lookback_start <= d <= today for d in bounce_dates):
        return min(BOUNCE_CAP, ramp_cap)
    return ramp_cap


def load_pipeline(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_pipeline(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    if not rows:
        return
    names = fieldnames or list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=names, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def _norm_status(status: str) -> str:
    return re.sub(r"\s+", " ", (status or "").strip().lower())


def pipeline_row_for(rows: Iterable[dict], company: str | None = None, email: str | None = None) -> dict | None:
    email_l = (email or "").strip().lower()
    company_l = (company or "").strip().lower()
    for row in rows:
        if email_l and (row.get("contact_detail") or "").strip().lower() == email_l:
            return row
        if company_l and (row.get("company") or "").strip().lower() == company_l:
            return row
    return None


def should_skip_followup(row: dict | None) -> str | None:
    """Return a skip reason if PIPELINE says this follow-up must not go out."""
    if row is None:
        return None
    status = _norm_status(row.get("status") or "")
    if status in SKIP_FOLLOWUP_STATUSES:
        return f"pipeline status {row.get('status')}"
    notes = (row.get("notes") or "") + " " + (row.get("outreach_sent") or "")
    if re.search(r"do[\s-]?not[\s-]?contact|opted out|unsubscribe reply", notes, re.I):
        if status not in {"contacted", "target"}:
            return "pipeline notes flag do-not-contact"
    return None


def is_opt_out_text(text: str) -> bool:
    return bool(OPT_OUT_RE.search(text or ""))


def mark_opted_out(row: dict, when: dt.date | None = None, note: str | None = None) -> dict:
    row = dict(row)
    row["status"] = "opted-out"
    row["next_follow_up"] = ""
    extra = note or "Opt-out / do-not-contact reply received; do not email again."
    day = (when or now_et().date()).isoformat()
    prev = (row.get("notes") or "").rstrip()
    tag = f"{day}: {extra}"
    row["notes"] = f"{prev} | {tag}" if prev else tag
    return row


def local_part(email: str) -> str:
    return (email or "").split("@", 1)[0].lower().split("+", 1)[0]


def classify_address(email: str) -> str:
    """preferred | named | other | generic. Never invents an address."""
    local = local_part(email)
    if not local or "@" not in (email or ""):
        return "generic"
    if local in PREFERRED_LOCAL or local.startswith("partner") or local.startswith("sponsor"):
        return "preferred"
    if local in GENERIC_LOCAL:
        return "generic"
    # A person-looking local part (jane, jane.doe, jane-doe) published on the site.
    if re.fullmatch(r"[a-z]+(?:[._-][a-z]+)+", local) or (
        re.fullmatch(r"[a-z]{2,20}", local) and local not in GENERIC_LOCAL | PREFERRED_LOCAL
        and local not in {"business", "marketing", "founders", "hello", "jobs", "careers", "security", "privacy", "legal"}
    ):
        # bare first names are too easy to misread; only dotted/hyphenated locals count as named
        if "." in local or "_" in local or "-" in local:
            return "named"
    return "other"


def select_published_contact(candidates: Iterable[dict]) -> dict | None:
    """Pick the best already-published address. Never guess or invent one.

    Each candidate is a dict with at least `email` and `source` (the page URL
    where it was found). Optional `role` may be 'partnerships', 'marketing',
    'devrel', or 'named-person'.
    """
    ranked: list[tuple[int, dict]] = []
    for c in candidates:
        email = (c.get("email") or "").strip()
        if not email or "@" not in email:
            continue
        kind = classify_address(email)
        role = (c.get("role") or "").lower()
        score = {"preferred": 300, "named": 200, "other": 100, "generic": 10}[kind]
        if role in {"partnerships", "sponsorships", "marketing", "devrel", "named-person"}:
            score += 50
        ranked.append((score, c))
    if not ranked:
        return None
    ranked.sort(key=lambda item: item[0], reverse=True)
    return ranked[0][1]


def thread_already_has_our_reply(messages: Iterable[dict]) -> bool:
    """True if Brandon or skillmaxx@ already sent a message in this thread."""
    for m in messages:
        blob = " ".join(
            str(m.get(k) or "") for k in ("fromAddress", "from", "sender", "fromName")
        ).lower()
        if any(n in blob for n in OUR_FROM_NEEDLES):
            return True
    return False
