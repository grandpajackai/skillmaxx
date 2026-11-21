#!/usr/bin/env python3
"""Offline tests for the Bluesky poster and weekly enqueue (no network, no secrets)."""
import os, subprocess, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def run(args, env=None):
    e = os.environ.copy()
    if env:
        e.update(env)
    # Make sure a leaked app password in the caller env cannot trigger a live path;
    # these tests only use --self-test / --dry-run / --list.
    return subprocess.run(args, cwd=ROOT, env=e, check=True, capture_output=True, text=True)

def test_self_test():
    r = run([sys.executable, "growth/social/bluesky_post.py", "--self-test"])
    assert "self-test ok" in r.stdout, r.stdout

def test_dry_run_lists_migrated_queue():
    r = run([sys.executable, "growth/social/bluesky_post.py", "--dry-run"])
    out = r.stdout
    assert "DRY-RUN" in out
    assert "buf-6afbc1c1df36f4d8256372d8" in out
    assert "buf-6afbc1c2797935b975d8a168" in out
    assert "buf-6afbc1cbdf36f4d8256375b2" in out
    assert "would post" in out or "not due yet" in out or "skip" in out

def test_buffer_weekly_dry_run():
    r = run([sys.executable, "growth/scripts/buffer_weekly.py", "--dry-run", "--repo-queue"])
    assert "no Buffer API" in r.stdout or "Grok Buffer connector" in r.stdout
    assert "Bluesky" in r.stdout

if __name__ == "__main__":
    test_self_test()
    test_dry_run_lists_migrated_queue()
    test_buffer_weekly_dry_run()
    print("test_bluesky_post ok")
