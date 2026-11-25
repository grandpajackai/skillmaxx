#!/usr/bin/env python3
"""Unit tests for outreach helpers. No network, no email."""
from __future__ import annotations

import datetime as dt
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "scripts"))

import lib  # noqa: E402
import outreach_config  # noqa: E402


class PostalTests(unittest.TestCase):
    def setUp(self):
        self._old = os.environ.pop("SKILLMAXX_POSTAL_ADDRESS", None)
        self._old_cfg = os.environ.pop("SKILLMAXX_OUTREACH_CONFIG", None)

    def tearDown(self):
        if self._old is None:
            os.environ.pop("SKILLMAXX_POSTAL_ADDRESS", None)
        else:
            os.environ["SKILLMAXX_POSTAL_ADDRESS"] = self._old
        if self._old_cfg is None:
            os.environ.pop("SKILLMAXX_OUTREACH_CONFIG", None)
        else:
            os.environ["SKILLMAXX_OUTREACH_CONFIG"] = self._old_cfg

    def test_unset_in_committed_config(self):
        # The committed config.env must stay empty until Brandon approves an address.
        os.environ.pop("SKILLMAXX_POSTAL_ADDRESS", None)
        os.environ.pop("SKILLMAXX_OUTREACH_CONFIG", None)
        self.assertEqual(outreach_config.postal_address(), "")
        with self.assertRaises(SystemExit) as ctx:
            outreach_config.require_postal_address()
        self.assertIn("SKILLMAXX_POSTAL_ADDRESS is unset", str(ctx.exception))

    def test_footer_and_require(self):
        os.environ["SKILLMAXX_POSTAL_ADDRESS"] = "123 Example St, Springfield, IL 62701"
        footer = lib.can_spam_footer()
        self.assertIn('Reply "no thanks"', footer)
        self.assertIn("123 Example St, Springfield, IL 62701", footer)
        body = lib.append_footer("Hi team,\n\nPitch here.\n\nBrandon")
        self.assertIn("Pitch here.", body)
        self.assertIn("123 Example St", body)
        self.assertEqual(body.count('Reply "no thanks"'), 1)

    def test_empty_env_holds_send(self):
        os.environ["SKILLMAXX_POSTAL_ADDRESS"] = "   "
        self.assertEqual(outreach_config.postal_address(), "")
        with self.assertRaises(SystemExit):
            lib.can_spam_footer()


class CapAndWindowTests(unittest.TestCase):
    def test_cap_drops_to_20_after_recent_bounce(self):
        today = dt.date(2026, 11, 25)
        self.assertEqual(lib.daily_cap(today, [dt.date(2026, 11, 19)]), 20)
        self.assertEqual(lib.daily_cap(today, [dt.date(2026, 11, 13)]), 30)
        self.assertEqual(lib.daily_cap(today, []), 30)

    def test_window_weekdays_9_to_5_et(self):
        wed = dt.datetime(2026, 11, 25, 9, 0, tzinfo=lib.ET)
        self.assertTrue(lib.in_send_window(wed))
        self.assertTrue(lib.in_send_window(wed.replace(hour=16, minute=59)))
        self.assertFalse(lib.in_send_window(wed.replace(hour=17)))
        self.assertFalse(lib.in_send_window(wed.replace(hour=8, minute=59)))
        sat = dt.datetime(2026, 11, 28, 11, 0, tzinfo=lib.ET)
        self.assertFalse(lib.in_send_window(sat))

    def test_gap_range(self):
        gaps = {lib.sleep_seconds() for _ in range(80)}
        self.assertTrue(all(20 * 60 <= g <= 60 * 60 for g in gaps))
        self.assertGreater(max(gaps) - min(gaps), 0)


class PipelineGateTests(unittest.TestCase):
    def test_skip_followup_statuses(self):
        for status in ("Bounced", "opted-out", "declined-warm", "Replied", "do-not-contact"):
            reason = lib.should_skip_followup({"status": status, "company": "X"})
            self.assertIsNotNone(reason, status)
        self.assertIsNone(lib.should_skip_followup({"status": "Contacted", "company": "X"}))
        self.assertIsNone(lib.should_skip_followup(None))

    def test_opt_out_phrases_and_mark(self):
        self.assertTrue(lib.is_opt_out_text('Please reply "no thanks" wait no: no thanks, take me off the list.'))
        self.assertTrue(lib.is_opt_out_text("Unsubscribe."))
        self.assertFalse(lib.is_opt_out_text("Thanks, interesting — tell me more about the $19 slot."))
        row = lib.mark_opted_out({"company": "X", "status": "Contacted", "notes": "src", "next_follow_up": "2026-11-30"}, when=dt.date(2026, 11, 25))
        self.assertEqual(row["status"], "opted-out")
        self.assertEqual(row["next_follow_up"], "")
        self.assertIn("do not email again", row["notes"])


class ContactSourcingTests(unittest.TestCase):
    def test_prefers_partnerships_over_hello(self):
        picked = lib.select_published_contact([
            {"email": "hello@example.com", "source": "https://example.com"},
            {"email": "partnerships@example.com", "source": "https://example.com/partners"},
        ])
        self.assertEqual(picked["email"], "partnerships@example.com")

    def test_prefers_named_person_over_sales(self):
        picked = lib.select_published_contact([
            {"email": "sales@example.com", "source": "https://example.com"},
            {"email": "jane.doe@example.com", "source": "https://example.com/team", "role": "devrel"},
        ])
        self.assertEqual(picked["email"], "jane.doe@example.com")

    def test_never_invents(self):
        self.assertIsNone(lib.select_published_contact([]))
        self.assertIsNone(lib.select_published_contact([{"email": "", "source": "x"}]))


class AutoReplyGuardTests(unittest.TestCase):
    def test_skips_when_we_already_replied(self):
        self.assertTrue(lib.thread_already_has_our_reply([
            {"fromAddress": "prospect@brand.com"},
            {"fromAddress": "Brandon at SkillMaxx <skillmaxx@gilventures.ai>"},
        ]))
        self.assertFalse(lib.thread_already_has_our_reply([
            {"fromAddress": "prospect@brand.com"},
        ]))


class ZohoGuardTests(unittest.TestCase):
    def setUp(self):
        self._old = os.environ.pop("SKILLMAXX_POSTAL_ADDRESS", None)

    def tearDown(self):
        if self._old is None:
            os.environ.pop("SKILLMAXX_POSTAL_ADDRESS", None)
        else:
            os.environ["SKILLMAXX_POSTAL_ADDRESS"] = self._old

    def test_zoho_send_refuses_when_unset(self):
        os.environ["SKILLMAXX_POSTAL_ADDRESS"] = ""
        import zoho_mail as z
        with self.assertRaises(SystemExit) as ctx:
            z.send("nobody@example.com", "subj", "body")
        self.assertIn("SKILLMAXX_POSTAL_ADDRESS is unset", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
