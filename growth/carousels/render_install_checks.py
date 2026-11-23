#!/usr/bin/env python3
"""Render the Nov 23 install-checks carousel as 1080x1080 PNGs.

Evergreen, tip-style deck: five practical checks before installing a skill,
plugin, or MCP server in Claude Code, Cursor, or Codex. Copy is grounded in
growth/social/POST-BANK.md (tips 1, 2, 8, 9, 10, 11), src/guides/cursor-mcp.njk,
and src/how-we-test.njk. No nightly scorecard figures, and no mention of
failures, regressions, or harness bugs.

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
/* Square (1080×1080) layout only. Type floors live in generate.BASE_CSS —
   do not shrink subtitles below 36px, body below 28px, or chrome below 22px. */
.slide { padding: 40px 52px 32px; }
.topbar { margin-bottom: 16px; }
.content { gap: 0; }
.visual { flex: 1; display: flex; flex-direction: column; justify-content: flex-start; min-height: 0; gap: 14px; margin-top: 4px; }
h1 { font-size: 60px; line-height: 1.05; margin-bottom: 12px; }
h2 { font-size: 48px; line-height: 1.1; margin-bottom: 12px; }
.cover-sub, .sub { font-size: 36px; line-height: 1.35; margin-bottom: 16px; color: #E5E7EB; }
.item-row { padding: 20px 24px; border-radius: 18px; flex: 1; align-items: center; }
.item-title { font-size: 32px; margin-bottom: 6px; }
.item-desc { font-size: 28px; line-height: 1.35; color: #E5E7EB; }
.note { font-size: 28px; padding-top: 14px; color: #E5E7EB; }
.footer { margin-top: 12px; padding-top: 12px; font-size: 24px; color: #D1D5DB; }
.cta-box, .nl-cta-box {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  background: linear-gradient(135deg, rgba(198,244,50,0.16), rgba(34,211,238,0.08));
  border: 2px solid rgba(198,244,50,0.62);
  border-radius: 22px;
  padding: 28px 32px;
  margin-top: 4px;
  box-shadow: 0 16px 46px rgba(0,0,0,0.55), 0 0 40px rgba(198,244,50,0.12);
}
.nl-url-pill, .cta-url-pill {
  display: inline-block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 28px;
  font-weight: 800;
  color: #0A0A0B;
  background: #C6F432;
  padding: 14px 22px;
  border-radius: 14px;
  margin: 16px 0 14px;
  letter-spacing: -0.01em;
}
.cta-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 22px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #C6F432;
  margin-bottom: 10px;
}
.cta-desc { font-size: 28px; color: #E5E7EB; line-height: 1.35; }
.cmd-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 0;
  background: #0E0E12;
  border: 1px solid rgba(198,244,50,0.32);
  border-radius: 20px;
  padding: 28px 32px;
}
.cmd-pill {
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 32px;
  font-weight: 700;
  color: #C6F432;
  background: transparent;
  border: none;
  border-radius: 0;
  padding: 0;
  letter-spacing: -0.02em;
  word-break: break-word;
}
.cmd-pill.inset {
  background: #0E0E12;
  border: 1px solid rgba(198,244,50,0.32);
  border-radius: 16px;
  padding: 16px 18px;
}
.cmd-kicker {
  font-family: 'JetBrains Mono', monospace;
  font-size: 22px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #D1D5DB;
  margin-bottom: 10px;
}
.pill-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
.pill-row .pill { font-size: 26px; padding: 12px 18px; }
.check-row {
  display: flex;
  align-items: center;
  gap: 18px;
  flex: 1;
  background: #121215;
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 16px;
  padding: 12px 20px;
  min-height: 0;
}
.check-row .rank-badge { width: 52px; height: 52px; font-size: 22px; border-radius: 14px; }
.check-copy { font-size: 28px; font-weight: 600; color: #EDEDEF; line-height: 1.25; }
.check-copy span { color: #D1D5DB; font-weight: 500; font-size: 28px; }
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


HOOK = """
<div class="eyebrow"><span class="dot"></span>SKILLS · PLUGINS · MCP SERVERS</div>
<h1>5 checks before you<br>install an <em>agent add-on</em>.</h1>
<p class="cover-sub">Practical steps we use when we install tools in Claude Code, Cursor, and Codex.</p>
<div class="visual">
  <div class="check-row"><div class="rank-badge">01</div><div class="check-copy">Pin the marketplace</div></div>
  <div class="check-row"><div class="rank-badge">02</div><div class="check-copy">Wait until Cursor says ready</div></div>
  <div class="check-row"><div class="rank-badge">03</div><div class="check-copy">Start with the official servers</div></div>
  <div class="check-row"><div class="rank-badge">04</div><div class="check-copy">Check more than one agent</div></div>
  <div class="check-row"><div class="rank-badge">05</div><div class="check-copy">Look up a real install first</div></div>
</div>
"""

TIP1 = """
<div class="eyebrow"><span class="dot"></span>CHECK 1 OF 5 · CLAUDE CODE</div>
<h2>Pin the <em>marketplace</em>.</h2>
<p class="sub">The @marketplace bit is not decoration. The same plugin name can live in more than one marketplace, and the agent will ask which one.</p>
<div class="visual">
  <div class="cmd-card">
    <div class="cmd-kicker">Claude Code</div>
    <div class="cmd-pill">/plugin install sentry@claude-plugins-official</div>
  </div>
</div>
<p class="note">Pin the source, then move on. This is the pattern we use on official marketplace plugins.</p>
"""

TIP2 = """
<div class="eyebrow"><span class="dot"></span>CHECK 2 OF 5 · CURSOR</div>
<h2>Wait until Cursor says <em>ready</em>.</h2>
<p class="sub">Add the server under mcpServers in ~/.cursor/mcp.json, then check the list. Anything else means it is not ready. Cursor is very literal.</p>
<div class="visual">
  <div class="cmd-card">
    <div class="cmd-kicker">Config file</div>
    <div class="cmd-pill">~/.cursor/mcp.json</div>
  </div>
  <div class="cmd-card">
    <div class="cmd-kicker">The line that counts</div>
    <div class="cmd-pill">ready</div>
  </div>
</div>
<p class="note">A project-level .cursor/mcp.json works the same way. We grade Cursor MCP on that exact line.</p>
"""

TIP3 = """
<div class="eyebrow"><span class="dot"></span>CHECK 3 OF 5 · MCP SERVERS</div>
<h2>Start with the <em>official</em> reference servers.</h2>
<p class="sub">They are still the backbone of most setups. Boring is a feature.</p>
<div class="visual">
  <div class="check-row"><div class="rank-badge">01</div><div class="check-copy">fetch</div></div>
  <div class="check-row"><div class="rank-badge">02</div><div class="check-copy">filesystem</div></div>
  <div class="check-row"><div class="rank-badge">03</div><div class="check-copy">git</div></div>
  <div class="check-row"><div class="rank-badge">04</div><div class="check-copy">memory</div></div>
  <div class="check-row"><div class="rank-badge">05</div><div class="check-copy">time</div></div>
</div>
<p class="note">The official MCP reference servers. We re-test them every night, alongside community packages.</p>
"""

TIP4 = """
<div class="eyebrow"><span class="dot"></span>CHECK 4 OF 5 · CLAUDE · CURSOR · CODEX</div>
<h2>Listed for one agent, <em>often works in more</em>.</h2>
<p class="sub">Most tools written for one agent also install in others. Check Claude Code, Cursor, and Codex before you assume it will not travel.</p>
<div class="visual">
  <div class="check-row"><div class="rank-badge">✓</div><div class="check-copy">Claude Code</div></div>
  <div class="check-row"><div class="rank-badge">✓</div><div class="check-copy">Cursor</div></div>
  <div class="check-row"><div class="rank-badge">✓</div><div class="check-copy">Codex</div></div>
  <div class="check-row"><div class="rank-badge">✓</div><div class="check-copy">Grok Build <span>and Pi, too</span></div></div>
</div>
<p class="note">MCP servers and standalone skills can be checked in all five agents we test.</p>
"""

TIP5 = """
<div class="eyebrow"><span class="dot"></span>CHECK 5 OF 5 · BEFORE YOU INSTALL</div>
<h2>Look up a <em>real install</em> first.</h2>
<p class="sub">Type the tool, pick your agent, and read last night's sandbox result. Two clean nights tell you more than a star count.</p>
<div class="visual">
  <div class="cmd-card">
    <div class="cmd-kicker">Is it safe to install today?</div>
    <div class="cmd-pill">skillmaxx.gilventures.ai/reports/latest/</div>
  </div>
</div>
<p class="note">Free, updated every night. Each result links to its install log.</p>
"""

CTA = """
<div class="eyebrow"><span class="dot"></span>FREE WEEKLY NEWSLETTER</div>
<h2>Tips, plus what actually <em>installed</em>, every Sunday.</h2>
<p class="sub">The free SkillMaxx newsletter is the weekly scorecard and the useful context around it.</p>
<div class="visual">
<div class="nl-cta-box">
  <div class="cta-label">Subscribe free</div>
  <div style="font-size:36px;font-weight:800;line-height:1.25;color:#EDEDEF">No hype. Just what works.</div>
  <div class="nl-url-pill">skillmaxx.gilventures.ai/newsletter/</div>
  <div class="cta-desc">Also the daily report and per-agent matrix, at the same site, $0.</div>
</div>
</div>
"""

X_HOOK = HOOK

X_TIPS_AB = """
<div class="eyebrow"><span class="dot"></span>CHECKS 1 AND 2</div>
<h2>Pin it. Then wait for <em>ready</em>.</h2>
<div class="visual">
  <div class="item-row">
    <div>
      <div class="item-title">01  Pin the marketplace</div>
      <div class="item-desc">In Claude Code, the @source is part of the command.</div>
      <div class="cmd-pill inset" style="font-size:26px;margin-top:12px">/plugin install sentry@claude-plugins-official</div>
    </div>
  </div>
  <div class="item-row">
    <div>
      <div class="item-title">02  Wait until Cursor says ready</div>
      <div class="item-desc">Add the server in ~/.cursor/mcp.json. Anything else means it is not ready.</div>
    </div>
  </div>
</div>
"""

X_TIPS_CDE = """
<div class="eyebrow"><span class="dot"></span>CHECKS 3, 4 AND 5</div>
<h2>Start simple. Then <em>look it up</em>.</h2>
<div class="visual">
  <div class="item-row"><div>
    <div class="item-title">03  Official reference servers first</div>
    <div class="item-desc">fetch, filesystem, git, memory, and time. Boring is a feature.</div>
  </div></div>
  <div class="item-row"><div>
    <div class="item-title">04  Check more than one agent</div>
    <div class="item-desc">Listed for one, often works in Claude Code, Cursor, and Codex too.</div>
  </div></div>
  <div class="item-row"><div>
    <div class="item-title">05  Look up a real install first</div>
    <div class="item-desc">skillmaxx.gilventures.ai/reports/latest/</div>
  </div></div>
</div>
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
    dest_root = ROOT / "src/assets/social/carousels/2026-11-23-install-checks"
    li_dir = dest_root
    x_dir = dest_root / "x"

    li = pack([HOOK, TIP1, TIP2, TIP3, TIP4, TIP5, CTA], "INSTALL TIPS")
    xs = pack([X_HOOK, X_TIPS_AB, X_TIPS_CDE, X_CTA], "INSTALL TIPS")

    li_pngs = render_set(li, li_dir)
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
