#!/usr/bin/env python3
"""Stdlib tests for testing/freshness.py. No network.

  python3 testing/test_freshness.py
"""
import os, shutil, sys, tempfile, unittest
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import freshness

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "fixtures", "freshness")
REPO = os.path.dirname(HERE)
ET = ZoneInfo("America/New_York")
NOW = datetime(2026, 11, 7, 12, 0, tzinfo=ET)
PAGE = "<p>Run started 2026-11-07T02:07-05:00. Every failed install is retried once.</p>"
OLDER = "<p>Run started 2026-11-06T02:02-05:00. Every failed install is retried once.</p>"


class FreshnessTest(unittest.TestCase):
    def assess(self, name, public=None):
        return freshness.assess(os.path.join(FIXTURES, name), now=NOW, public=public)

    def test_nopush_done_is_local_success_not_a_deploy(self):
        st = self.assess("nopush")
        self.assertEqual(st["local_state"], "ok")
        self.assertEqual(st["last_success"], "2026-11-07T02:34:00-05:00")
        self.assertTrue(st["nopush"])
        self.assertTrue(st["local_build_completed"])
        self.assertFalse(st["local_build_is_public_deploy"])
        self.assertIsNone(st["published_at"])
        self.assertEqual(st["publish_state"], "not_pushed")
        self.assertFalse(st["checked_public"])
        self.assertFalse(st["live_page_matches_local_results"])
        self.assertEqual(st["test_run_at"], "2026-11-07T02:07-05:00")
        self.assertEqual(st["report_run_at"], "2026-11-07T02:07-05:00")
        self.assertEqual(st["tests_pass"], 1)
        self.assertEqual(st["tests_total"], 2)
        self.assertIn("did not push", st["summary"])
        self.assertIn("not a public deploy", st["summary"])
        self.assertIsNone(st["repo_nightly_commit"])

    def test_trial_log_is_not_a_push_and_failures_still_finish(self):
        st = freshness.assess(os.path.join(FIXTURES, "trial"), now=datetime(2026, 11, 7, 18, 0, tzinfo=ET))
        self.assertEqual(st["local_state"], "ok")
        self.assertEqual(st["last_success"], "2026-11-07T16:28:27-05:00")
        self.assertTrue(st["nopush"])
        self.assertEqual(st["publish_state"], "not_pushed")
        self.assertIsNone(st["published_at"])
        self.assertFalse(st["local_build_is_public_deploy"])
        self.assertEqual(st["tests_pass"], 1)
        self.assertEqual(st["tests_total"], 2)
        self.assertNotEqual(st["tests_pass"], 775)
        self.assertIn("did not push", st["summary"])
        self.assertIn("reached done", st["summary"])
        self.assertIn("separate from whether the pipeline finished", st["summary"])
        self.assertNotIn("Log has no NOPUSH line", " ".join(st["notes"]))
        self.assertNotIn("all pass", st["summary"].lower())

    def test_trailing_lock_skip_does_not_erase_success(self):
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root)
        src = os.path.join(FIXTURES, "nopush")
        shutil.copytree(src, root, dirs_exist_ok=True)
        log = os.path.join(root, "testing", "logs", "nightly-2026-11-07.log")
        with open(log, "a", encoding="utf-8") as f:
            f.write("\nanother nightly is running\n")
        st = freshness.assess(root, now=NOW)
        self.assertEqual(st["local_state"], "ok")
        self.assertEqual(st["publish_state"], "not_pushed")
        self.assertEqual(st["last_success"], "2026-11-07T02:34:00-05:00")

    def test_build_failure_is_error_and_not_published(self):
        st = self.assess("failed")
        self.assertEqual(st["local_state"], "error")
        self.assertEqual(st["failed_step"], "eleventy build")
        self.assertIsNone(st["last_success"])
        self.assertFalse(st["local_build_completed"])
        self.assertFalse(st["local_build_is_public_deploy"])
        self.assertIsNone(st["published_at"])
        self.assertEqual(st["publish_state"], "unverified")
        self.assertIn("eleventy build", st["summary"])

    def test_old_success_is_stale(self):
        st = self.assess("stale")
        self.assertEqual(st["local_state"], "stale")
        self.assertEqual(st["last_success"], "2026-11-05T02:41:05-05:00")
        self.assertIsNone(st["published_at"])
        self.assertFalse(st["nopush"])
        self.assertIn("older than", st["summary"])

    def test_results_alone_are_not_success_or_publish(self):
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root)
        dest = os.path.join(root, "testing", "results")
        os.makedirs(dest)
        shutil.copy(os.path.join(FIXTURES, "nopush", "testing", "results", "2026-11-07.json"), dest)
        st = freshness.assess(root, now=NOW)
        self.assertEqual(st["local_state"], "unknown")
        self.assertIsNone(st["last_success"])
        self.assertIsNone(st["published_at"])
        self.assertEqual(st["publish_state"], "unverified")
        self.assertEqual(st["test_run_at"], "2026-11-07T02:07-05:00")
        self.assertFalse(st["live_page_matches_local_results"])

    def test_public_match_does_not_hide_nopush(self):
        public = {"ok": True, "error": None, "page": PAGE, "page_url": freshness.LIVE_URL,
                  "published_at": "2026-11-07T07:50:12Z",
                  "published_at_source": "https://api.github.com/repos/grandpajackai/skillmaxx/deployments/1/statuses"}
        st = self.assess("nopush", public=public)
        self.assertTrue(st["live_page_matches_local_results"])
        self.assertEqual(st["publish_state"], "not_pushed")
        self.assertEqual(st["published_at"], "2026-11-07T07:50:12Z")
        self.assertFalse(st["local_build_is_public_deploy"])
        self.assertTrue(any("did not push" in n for n in st["notes"]))
        self.assertIn("GitHub Pages", st["summary"])

    def test_public_mismatch_is_not_a_deploy_of_this_run(self):
        public = {"ok": True, "error": None, "page": OLDER, "page_url": freshness.LIVE_URL,
                  "published_at": "2026-11-06T08:00:00Z", "published_at_source": freshness.DEPLOY_API}
        st = self.assess("nopush", public=public)
        self.assertFalse(st["live_page_matches_local_results"])
        self.assertEqual(st["publish_state"], "not_pushed")
        self.assertEqual(st["public_report_run_at"], "2026-11-06T02:02-05:00")
        self.assertNotEqual(st["published_at"], st["last_success"])

    def test_deploy_time_without_a_page_is_not_a_content_match(self):
        public = {"ok": False, "error": "Live page fetch failed.", "page": "",
                  "published_at": "2026-11-07T07:50:12Z", "published_at_source": freshness.DEPLOY_API}
        st = self.assess("stale", public=public)
        self.assertEqual(st["published_at"], "2026-11-07T07:50:12Z")
        self.assertEqual(st["publish_state"], "unverified")
        self.assertFalse(st["live_page_matches_local_results"])

    def test_unreachable_public_check_does_not_invent_published_at(self):
        public = {"ok": False, "error": "Live page fetch failed: timed out.", "page": "",
                  "published_at": None, "published_at_source": None}
        st = self.assess("stale", public=public)
        self.assertIsNone(st["published_at"])
        self.assertEqual(st["publish_state"], "unreachable")
        self.assertFalse(st["live_page_matches_local_results"])
        nopush = self.assess("nopush", public=public)
        self.assertEqual(nopush["publish_state"], "not_pushed")
        self.assertIsNone(nopush["published_at"])

    def test_live_match_without_nopush(self):
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root)
        shutil.copytree(os.path.join(FIXTURES, "nopush"), root, dirs_exist_ok=True)
        log = os.path.join(root, "testing", "logs", "nightly-2026-11-07.log")
        with open(log, encoding="utf-8") as f:
            text = f.read().replace("NOPUSH set, not pushing\n", "")
        with open(log, "w", encoding="utf-8") as f:
            f.write(text)
        public = {"ok": True, "error": None, "page": PAGE, "page_url": freshness.LIVE_URL,
                  "published_at": None, "published_at_source": None}
        st = freshness.assess(root, now=NOW, public=public)
        self.assertFalse(st["nopush"])
        self.assertEqual(st["publish_state"], "live_matches")
        self.assertIsNone(st["published_at"])
        self.assertTrue(st["live_page_matches_local_results"])
        self.assertIn("No GitHub Pages deployment time was verified", st["summary"])

    def test_writes_json_md_html(self):
        out = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, out)
        st = self.assess("nopush")
        paths = freshness.write_status(st, out)
        for name in ("freshness.json", "freshness.md", "freshness.html"):
            self.assertTrue(os.path.isfile(paths[name]))
            with open(paths[name], encoding="utf-8") as f:
                body = f.read()
            self.assertIn("2026-11-07T02:34:00-05:00", body)
            self.assertIn("not_pushed", body)
            self.assertIn("python3 testing/freshness.py", body)
            if name == "freshness.html":
                self.assertNotIn("<script", body)

    def test_newest_pages_success_picks_latest(self):
        deployments = [
            {"statuses_url": "old", "sha": "aaa"},
            {"statuses_url": "new", "sha": "bbb"},
        ]
        seen = []

        def fake_get(url, timeout=20):
            seen.append(url)
            if url == "old":
                return 200, '[{"state":"success","created_at":"2026-11-06T08:00:00Z"}]'
            return 200, '[{"state":"success","created_at":"2026-11-07T07:50:12Z"},{"state":"failure","created_at":"2026-11-07T07:40:00Z"}]'

        real = freshness._http_get
        freshness._http_get = fake_get
        try:
            at, src, sha = freshness._newest_pages_success(deployments, 5)
        finally:
            freshness._http_get = real
        self.assertEqual(at, "2026-11-07T07:50:12Z")
        self.assertEqual(src, "new")
        self.assertEqual(sha, "bbb")
        self.assertEqual(seen, ["old", "new"])

    def test_nightly_hook_is_local_only(self):
        with open(os.path.join(REPO, "testing", "nightly.sh"), encoding="utf-8") as f:
            text = f.read()
        self.assertIn("testing/freshness.py --quiet", text)
        self.assertNotIn("freshness.py --check-public", text)
        self.assertNotIn("testing/status", text.split("ADD=")[1].split("git add", 1)[0])

    def test_this_checkout_does_not_invent_a_deploy(self):
        st = freshness.assess(REPO, now=NOW)
        self.assertIsNone(st["published_at"])
        self.assertIsNone(st["last_success"])
        self.assertEqual(st["local_state"], "unknown")
        self.assertEqual(st["publish_state"], "unverified")
        self.assertFalse(st["local_build_is_public_deploy"])
        self.assertFalse(st["live_page_matches_local_results"])
        self.assertRegex(st["test_run_at"] or "", r"^2026-11-")
        if st["repo_nightly_commit"]:
            self.assertIn("nightly refresh", st["repo_nightly_commit"]["subject"])
            self.assertNotEqual(st["repo_nightly_commit"]["committed_at"], st["published_at"])


if __name__ == "__main__":
    unittest.main()
