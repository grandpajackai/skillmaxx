"""Helpers for an optional inquiry auto-acknowledgement. This module does not send mail."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "outreach"))
from lib import thread_already_has_our_reply  # noqa: E402

HERE = Path(__file__).resolve().parent


def load_template(kind: str) -> str:
    names = {
        "advertise": "autoresponse-advertise.txt",
        "sponsor-inquiry": "autoresponse-advertise.txt",
        "submit": "autoresponse-submit.txt",
    }
    path = HERE / names[kind]
    return path.read_text(encoding="utf-8")


def should_send_auto_reply(thread_messages: list[dict]) -> tuple[bool, str]:
    """Return (ok, reason). Never send if we already replied in the thread."""
    if thread_already_has_our_reply(thread_messages):
        return False, "skip: Brandon or skillmaxx@ already replied in this thread"
    return True, "ok"
