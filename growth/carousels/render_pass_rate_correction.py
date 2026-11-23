#!/usr/bin/env python3
"""Render the Nov 23 Issue #4 pass-rate correction carousel as 1080x1080 PNGs.

All figures are from committed sources:
  - src/newsletter/issue-4.md and src/_data/weeks.json (week 2026-47)
  - src/_data/reports.json nights Nov 14 and Nov 17-22
  - STATUS.md 2026-11-22 session log + PR #151 (harness race diagnosis)

Does not post or talk to Buffer.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

import generate as g  # noqa: E402

SQUARE_CSS = """
.slide { padding: 48px 56px 40px; }
.topbar { margin-bottom: 22px; }
.brand { font-size: 24px; gap: 12px; }
.tag, .page-num { font-size: 14px; padding: 6px 12px; }
.eyebrow { font-size: 15px; padding: 7px 14px; margin-bottom: 16px; }
.dot { width: 8px; height: 8px; }
.visual { flex: 1; display: flex; flex-direction: column; justify-content: center; min-height: 0; gap: 14px; }
h1 { font-size: 58px; line-height: 1.06; margin-bottom: 16px; }
h2 { font-size: 42px; line-height: 1.12; margin-bottom: 14px; }
.cover-sub, .sub { font-size: 24px; line-height: 1.4; margin-bottom: 22px; color: #A1A1AA; }
.stat-grid { gap: 14px; margin-bottom: 0; margin-top: 8px; }
.stat-card { padding: 28px 24px 24px; border-radius: 18px; }
.stat-val { font-size: 56px; margin-bottom: 8px; }
.stat-lbl { font-size: 16px; line-height: 1.3; }
.item-row { padding: 22px 24px; border-radius: 18px; }
.item-title { font-size: 24px; margin-bottom: 6px; }
.item-desc { font-size: 18px; line-height: 1.4; }
.bar-row { padding: 10px 18px; border-radius: 14px; }
.bar-head { margin-bottom: 8px; }
.bar-name { font-size: 20px; }
.bar-nums { font-size: 20px; }
.track { height: 12px; }
.note { font-size: 16px; padding-top: 14px; }
.footer { margin-top: 14px; padding-top: 14px; font-size: 15px; }
.cta-box, .nl-cta-box {
  background: linear-gradient(135deg, rgba(198,244,50,0.16), rgba(34,211,238,0.08));
  border: 2px solid rgba(198,244,50,0.62);
  border-radius: 22px;
  padding: 26px 28px;
  margin-top: 10px;
  box-shadow: 0 16px 46px rgba(0,0,0,0.55), 0 0 40px rgba(198,244,50,0.12);
}
.nl-url-pill, .cta-url-pill {
  display: inline-block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 22px;
  font-weight: 800;
  color: #0A0A0B;
  background: #C6F432;
  padding: 12px 20px;
  border-radius: 14px;
  margin: 14px 0 12px;
  letter-spacing: -0.01em;
}
.cta-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #C6F432;
  margin-bottom: 8px;
}
.delta-row {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 16px;
  align-items: stretch;
  margin-top: 8px;
}
.delta-arrow {
  display: grid;
  place-items: center;
  font-family: 'JetBrains Mono', monospace;
  font-size: 28px;
  font-weight: 700;
  color: #8A8F98;
}
.night-list { display: flex; flex-direction: column; gap: 8px; }
"""


def wrap(body: str, idx: int, total: int, badge: str, footer_right: str) -> str:
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><style>{g.font_css()}{g.base_css()}{SQUARE_CSS}</style></head>
<body>
  <div class="slide">
    <div class="topbar">
      <div class="brand">{g.brand_mark(40)}<div>Skill<span>Maxx</span></div></div>
      <div class="top-meta">
        <div class="tag">{g.esc(badge)}</div>
        <div class="page-num">{idx:02d} / {total:02d}</div>
      </div>
    </div>
    <div class="content">{body}</div>
    <div class="footer">
      <div><b>skillmaxx.gilventures.ai</b></div>
      <div>{g.esc(footer_right)}</div>
    </div>
  </div>
</body></html>"""


def pack(bodies: list[str], badge: str) -> list[str]:
    total = len(bodies)
    out = []
    for i, body in enumerate(bodies, 1):
        right = "Swipe →" if i < total else "Free Sunday newsletter"
        out.append(wrap(body, i, total, badge, right))
    return out


# --- Shared slide bodies (numbers locked to issue #4 / week 2026-47 / PR #151) ---

HOOK = """
<div class="eyebrow"><span class="dot"></span>ISSUE #4 · NOV 16–22, 2026</div>
<h1>Our pass rate fell<br><em>9.4 points</em> this week.</h1>
<p class="cover-sub">Then we found out why.</p>
<div class="visual">
<div class="delta-row">
  <div class="stat-card">
    <div class="stat-val">87.1%</div>
    <div class="stat-lbl">Nov 14 · 910 of 1,045 judged</div>
  </div>
  <div class="delta-arrow">→</div>
  <div class="stat-card">
    <div class="stat-val lime">77.7%</div>
    <div class="stat-lbl">Nov 22 · 831 of 1,070 judged</div>
  </div>
</div>
</div>
"""

SCORE = """
<div class="eyebrow"><span class="dot"></span>PUBLISHED SCORECARD · NOV 22</div>
<h2><em>831</em> of 1,085 installs passed.</h2>
<p class="sub">77.7% of the 1,070 we can judge without an API key. Fifteen more only needed a key, which is not a defect.</p>
<div class="visual">
<div class="stat-grid" style="grid-template-columns: 1fr 1fr; margin: 0;">
  <div class="stat-card"><div class="stat-val lime">77.7%</div><div class="stat-lbl">Judgeable pass rate, Nov 22</div></div>
  <div class="stat-card"><div class="stat-val">9.4</div><div class="stat-lbl">Points down from Nov 14 (87.1%)</div></div>
</div>
</div>
<p class="note">Source: SkillMaxx Weekly issue #4, from the Nov 17–22 nightly logs.</p>
"""

TREND = """
<div class="eyebrow"><span class="dot"></span>WEEK 2026-47 · NIGHT BY NIGHT</div>
<h2>The drop arrived in the <em>last two nights</em>.</h2>
<div class="visual"><div class="night-list">
  <div class="bar-row"><div class="bar-head"><div class="bar-name">Nov 17</div><div class="bar-nums">86.8%<span>911 / 1,050</span></div></div><div class="track"><div class="fill" style="width:86.8%"></div></div></div>
  <div class="bar-row"><div class="bar-head"><div class="bar-name">Nov 18</div><div class="bar-nums">86.9%<span>912 / 1,050</span></div></div><div class="track"><div class="fill" style="width:86.9%"></div></div></div>
  <div class="bar-row"><div class="bar-head"><div class="bar-name">Nov 19</div><div class="bar-nums">86.3%<span>906 / 1,050</span></div></div><div class="track"><div class="fill" style="width:86.3%"></div></div></div>
  <div class="bar-row"><div class="bar-head"><div class="bar-name">Nov 20</div><div class="bar-nums">86.3%<span>906 / 1,050</span></div></div><div class="track"><div class="fill" style="width:86.3%"></div></div></div>
  <div class="bar-row"><div class="bar-head"><div class="bar-name">Nov 21</div><div class="bar-nums">81.3%<span>862 / 1,060</span></div></div><div class="track"><div class="fill" style="width:81.3%;background:#FCD34D"></div></div></div>
  <div class="bar-row"><div class="bar-head"><div class="bar-name">Nov 22</div><div class="bar-nums">77.7%<span>831 / 1,070</span></div></div><div class="track"><div class="fill" style="width:77.7%;background:#FCA5A5"></div></div></div>
</div></div>
<p class="note">Share of installs we can judge without an API key. Week 2026-47 reports.</p>
"""

WEEK_LOG = """
<div class="eyebrow"><span class="dot"></span>WEEK 47 PUBLISHED LOG</div>
<h2>What the week log <em>shows</em>.</h2>
<div class="visual">
<div class="stat-grid" style="grid-template-columns: 1fr 1fr; margin: 0;">
  <div class="stat-card"><div class="stat-val" style="color:#86EFAC">5</div><div class="stat-lbl">Installs that started working</div></div>
  <div class="stat-card"><div class="stat-val" style="color:#FCA5A5">68</div><div class="stat-lbl">Newly broken installs, across 25 add-ons</div></div>
  <div class="stat-card"><div class="stat-val" style="color:#FCD34D">31</div><div class="stat-lbl">Add-ons that flipped pass / fail</div></div>
  <div class="stat-card"><div class="stat-val">203</div><div class="stat-lbl">Total broken installs on Nov 22</div></div>
</div>
</div>
<p class="note">Newly broken means failed two nights running. These are the published counts, including the late-week harness failures on the next slide.</p>
"""

CATCH = """
<div class="eyebrow"><span class="dot"></span>THE CATCH · PR #151</div>
<h2>The late-week slide was<br><em>our harness</em>, not the tools.</h2>
<div class="visual">
<div class="card-stack" style="gap:16px">
  <div class="item-row"><div><div class="item-title">91 regressions, all on 25 npx MCP servers</div><div class="item-desc">Traced from the Nov 20 to Nov 22 drop (906 passing down to 831).</div></div></div>
  <div class="item-row"><div><div class="item-title">0 regressions outside those npx servers</div><div class="item-desc">No non-npx add-on newly failed in that slide.</div></div></div>
</div>
</div>
<p class="note">The published 68 / 203 counts include those false failures. The add-ons were not all newly broken.</p>
"""

FIX = """
<div class="eyebrow"><span class="dot"></span>WHAT WE CHANGED</div>
<h2>Parallel tests shared one npm extract folder.</h2>
<p class="sub">Six sandboxes ran at once, installs collided, and clean tools looked broken.</p>
<div class="visual">
<div class="card-stack" style="gap:16px">
  <div class="item-row"><div><div class="item-title">The race</div><div class="item-desc">Shared extract folders let two installs overwrite each other, so a passing package was recorded as a fail.</div></div></div>
  <div class="item-row"><div><div class="item-title">The fix, in PR #151</div><div class="item-desc">Each sandbox now gets its own extract folder. The next nights will show the real pass rate, not a bug in our tools.</div></div></div>
</div>
</div>
"""

CTA = """
<div class="eyebrow"><span class="dot"></span>FREE WEEKLY NEWSLETTER</div>
<h2>The numbers, with the context, <em>every Sunday</em>.</h2>
<p class="sub" style="margin-bottom:0">Issue #4 is up now, including this week&apos;s scorecard and the nightly links.</p>
<div class="visual">
<div class="nl-cta-box">
  <div class="cta-label">Subscribe free</div>
  <div style="font-size:28px;font-weight:800;line-height:1.25">No hype. Just the install logs.</div>
  <div class="nl-url-pill">skillmaxx.gilventures.ai/newsletter/</div>
  <div class="cta-desc" style="font-size:18px;color:#9CA3AF;line-height:1.4">Also the daily report and per-agent matrix, at the same site, $0.</div>
</div>
</div>
"""

# Compact X versions (same facts, less copy)
X_HOOK = HOOK

X_SCORE = """
<div class="eyebrow"><span class="dot"></span>PUBLISHED SCORECARD · NOV 22</div>
<h2><em>831</em> of 1,085 installs passed.</h2>
<p class="sub">77.7% of the 1,070 we can judge without an API key, down from 87.1% on Nov 14.</p>
<div class="visual">
<div class="delta-row">
  <div class="stat-card"><div class="stat-val">87.1%</div><div class="stat-lbl">Nov 14 · 910 of 1,045</div></div>
  <div class="delta-arrow">→</div>
  <div class="stat-card"><div class="stat-val lime">77.7%</div><div class="stat-lbl">Nov 22 · 831 of 1,070</div></div>
</div>
</div>
<p class="note">The published week log also lists 68 newly broken installs across 25 add-ons, and 203 broken on Nov 22.</p>
"""

X_CATCH = """
<div class="eyebrow"><span class="dot"></span>THE CATCH · PR #151</div>
<h2>That late-week drop was<br><em>our harness</em>, not the tools.</h2>
<div class="visual">
<div class="card-stack" style="gap:16px">
  <div class="item-row"><div><div class="item-title">91 regressions, all on 25 npx MCP servers</div><div class="item-desc">From 906 passing on Nov 20 down to 831 on Nov 22.</div></div></div>
  <div class="item-row"><div><div class="item-title">0 regressions outside those servers</div><div class="item-desc">Parallel sandboxes shared one npm extract folder. Installs collided and clean tools looked broken.</div></div></div>
</div>
</div>
<p class="note">We fixed it in PR #151. The next nights will show the real pass rate.</p>
"""

X_CTA = CTA


def render_set(slides: list[str], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    return g.render_slides_html(slides, out_dir)


def write_pdf(pngs: list[Path], dest: Path) -> None:
    from PIL import Image

    images = [Image.open(p).convert("RGB") for p in pngs]
    if not images:
        raise SystemExit("no pngs for pdf")
    images[0].save(dest, save_all=True, append_images=images[1:], resolution=72)
    for im in images:
        im.close()


def main() -> int:
    g.set_render(width=1080, height=1080, cta="newsletter")
    dest_root = ROOT / "src/assets/social/carousels/2026-11-23-pass-rate-correction"
    li_dir = dest_root
    x_dir = dest_root / "x"

    li = pack([HOOK, SCORE, TREND, WEEK_LOG, CATCH, FIX, CTA], "ISSUE #4")
    xs = pack([X_HOOK, X_SCORE, X_CATCH, X_CTA], "ISSUE #4")

    li_pngs = render_set(li, li_dir)
    # render_set writes slide-01.. into li_dir; x should be a subfolder.
    # But render also might leave only slides. Move/write x separately after.
    x_pngs = render_set(xs, x_dir)
    pdf_path = dest_root / "carousel.pdf"
    write_pdf(li_pngs, pdf_path)
    print(f"linkedin {len(li_pngs)} slides + {pdf_path.name} -> {li_dir}")
    print(f"x        {len(x_pngs)} slides -> {x_dir}")
    for p in li_pngs + x_pngs + [pdf_path]:
        print(f"  {p.relative_to(ROOT)}  {p.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
