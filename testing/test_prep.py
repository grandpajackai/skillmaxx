#!/usr/bin/env python3
"""Offline smoke test for growth/prep/prep.py: every job writes .md/.json, no network, no Zoho, no sends."""
import json, os, subprocess, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PREP = os.path.join(ROOT, "growth", "prep", "prep.py")
SRC = open(PREP, encoding="utf-8").read()


def main():
    # Guard: the prep script must never call a sending/posting path.
    for bad in ("zoho_mail.send", "zoho_mail.call(\"POST\"", "createRecord", "com.atproto.repo", "api.twitter.com", "api.x.com"):
        assert bad not in SRC, f"prep.py must not contain {bad}"
    with tempfile.TemporaryDirectory() as out:
        for job in ("xradar", "queue", "bluesky", "outreach", "pipeline", "recap"):
            r = subprocess.run([sys.executable, PREP, job, "--offline", "--date", "2026-11-18", "--out", out],
                               capture_output=True, text=True, env={**os.environ, "PATH": "/nonexistent"})
            assert r.returncode == 0, f"{job}: {r.stderr[-800:]}"
            md = open(os.path.join(out, job + ".md"), encoding="utf-8").read()
            meta = json.load(open(os.path.join(out, job + ".json"), encoding="utf-8"))["meta"]
            assert meta["date"] == "2026-11-18" and '"date": "2026-11-18"' in md.splitlines()[1], job
            if job == "recap":
                nl = open(os.path.join(out, "newsletter-draft.md"), encoding="utf-8").read()
                assert "permalink: false" in nl and "eleventyExcludeFromCollections: true" in nl, "draft must never build"
            print(f"ok {job}: {len(md.splitlines())} lines")
    print("test_prep: all ok")


if __name__ == "__main__":
    main()
