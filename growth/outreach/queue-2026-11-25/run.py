#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_day
if __name__ == "__main__":
    if "--date" not in sys.argv:
        sys.argv[1:1] = ["--date", "2026-11-25"]
    run_day.main()
