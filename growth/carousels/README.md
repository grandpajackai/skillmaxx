# SkillMaxx Carousel Generator

Free, local PNG and animated MP4 carousel generator for Instagram, LinkedIn, X (1080×1350) and TikTok Photo Mode (1080×1920).

Reads only committed nightly test data (`src/_data/reports.json`, `src/_data/weeks.json`, `src/_data/latestRows.json`, `data/skills.json`, `data/meta/meta.json`) and renders HTML/CSS slides with bundled `Inter` and `JetBrains Mono` fonts via headless Chromium. The `timely` format also pulls a fresh, keyless Hacker News radar (`growth/scripts/fetch_radar_hn.py`) at render time. With `--animate` (requires `ffmpeg` + Python `playwright`), records deterministic 30fps H.264 (`yuv420p`) MP4 slides, final-frame PNG fallbacks, and a stitched `preview.mp4`. Never posts or queues to Buffer.

The weekly editorial plan is in [CONTENT-PLAN.md](CONTENT-PLAN.md). The default CTA is the free newsletter; `--cta keyword` and `--cta hybrid` are placeholders until Brandon chooses a fulfillment path.

## Usage

```bash
python3 growth/carousels/generate.py --format all --out /workspace/carousels-samples --zip
python3 growth/carousels/generate.py --format v3 --size both --cta newsletter --out /workspace/carousels-samples --zip
python3 growth/carousels/generate.py --format v3 --animate --size both --out /workspace/carousels-samples --zip
python3 growth/carousels/generate.py --format timely --date 2026-11-20 --out /tmp/carousels
python3 growth/carousels/generate.py --format timely --stub --size both --out /tmp/carousels --zip
python3 growth/carousels/generate.py --format news --date 2026-11-20 --out /tmp/carousels
python3 growth/carousels/generate.py --format leaderboard --out /tmp/carousels
```

`--size 1080x1350|1080x1920|both` (default 1080×1350). `--v3` upgrades orgchart/maxxing to the 8–10 slide structure. `--format v3` renders orgchart, maxxing, and timely.
