#!/usr/bin/env python3
"""Offline test for testing/write_marketing_status.py: --out dry-run, required keys, no '@'."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "testing" / "write_marketing_status.py"
REQUIRED = (
    "name",
    "owner",
    "light",
    "headline",
    "kpis",
    "details",
    "issues",
    "needs",
    "needs_brandon",
    "updated_at",
)


def main() -> int:
    assert SCRIPT.is_file(), SCRIPT
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "marketing-status.json"
        r = subprocess.run(
            [sys.executable, str(SCRIPT), "--out", str(out), "--repo", str(ROOT), "--state", td],
            capture_output=True,
            text=True,
            env={**os.environ, "BEEHIIV_API_KEY": "", "SKILLMAXX_BEEHIIV_ENV": str(Path(td) / "missing.env")},
        )
        assert r.returncode == 0, f"exit {r.returncode}: {r.stderr}\n{r.stdout}"
        assert out.is_file(), "did not write --out path"
        doc = json.loads(out.read_text(encoding="utf-8"))
        missing = [k for k in REQUIRED if k not in doc]
        assert not missing, missing
        assert doc["schema_version"] == 1
        assert doc["name"] == "SkillMaxx"
        assert doc["owner"] == "SkillMaxx CEO"
        assert doc["light"] in {"green", "yellow", "red", "grey"}
        assert isinstance(doc["headline"], list)
        assert isinstance(doc["kpis"], dict)
        assert isinstance(doc["details"], list)
        assert isinstance(doc["issues"], list)
        assert isinstance(doc["needs"], list)
        assert isinstance(doc["needs_brandon"], list)
        assert any("carousel CTA" in x for x in doc["needs_brandon"])
        blob = json.dumps(doc, ensure_ascii=False)
        assert "@" not in blob, "status document must not contain @"
        # Atomic write leftover should not remain.
        assert not (out.parent / (out.name + ".tmp")).exists()
        print("test_marketing_status: ok")
        return 0


if __name__ == "__main__":
    sys.exit(main())
