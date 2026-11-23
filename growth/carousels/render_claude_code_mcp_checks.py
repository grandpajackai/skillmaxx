#!/usr/bin/env python3
"""Render the Nov 23 Claude Code MCP checks carousel as 1080x1080 PNGs.

One reader, one tool: a developer using Claude Code who installed an MCP
server and still cannot see it. Copy is grounded in official Anthropic
docs (code.claude.com/docs/en/mcp, plugins/install, skills) and in
src/how-we-test.njk (the npx cold-start note and the SkillMaxx lookup).
No scorecard-drop figures, and no SkillMaxx failure story.

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
h1 { font-size: 56px; line-height: 1.08; margin-bottom: 12px; }
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
  padding: 24px 28px;
}
.cmd-pill {
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 30px;
  font-weight: 700;
  color: #C6F432;
  background: transparent;
  border: none;
  border-radius: 0;
  padding: 0;
  letter-spacing: -0.02em;
  word-break: break-word;
  white-space: pre-wrap;
  line-height: 1.35;
}
.cmd-pill.inset {
  background: #0E0E12;
  border: 1px solid rgba(198,244,50,0.32);
  border-radius: 16px;
  padding: 16px 18px;
  font-size: 28px;
  line-height: 1.4;
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
.pill-row .pill { font-size: 28px; padding: 12px 18px; }
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
.check-row .rank-badge { width: 52px; height: 52px; font-size: 22px; border-radius: 14px; flex-shrink: 0; }
.check-copy { font-size: 28px; font-weight: 600; color: #EDEDEF; line-height: 1.25; }
.check-copy span { color: #D1D5DB; font-weight: 500; font-size: 28px; }
.check-copy b { color: #C6F432; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
.status-row {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  flex: 1;
  background: #121215;
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 16px;
  padding: 14px 20px;
  min-height: 0;
}
.status-mark {
  font-family: 'JetBrains Mono', monospace;
  font-size: 28px;
  font-weight: 700;
  color: #C6F432;
  flex-shrink: 0;
  width: 36px;
  line-height: 1.2;
}
.status-row.neutral .status-mark { color: #E5E7EB; }
.status-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 28px;
  font-weight: 700;
  color: #EDEDEF;
  line-height: 1.25;
  margin-bottom: 4px;
}
.status-desc { font-size: 28px; color: #E5E7EB; line-height: 1.3; }
.scope-name {
  font-family: 'JetBrains Mono', monospace;
  font-size: 28px;
  font-weight: 700;
  color: #C6F432;
  min-width: 120px;
  flex-shrink: 0;
}
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
<div class="eyebrow"><span class="dot"></span>CLAUDE CODE · MCP SERVERS</div>
<h1>Your MCP is installed.<br>Claude Code still <em>can't see it</em>.</h1>
<p class="cover-sub">Check these 5 things before you tear the config apart.</p>
<div class="visual">
  <div class="check-row"><div class="rank-badge">01</div><div class="check-copy">Run <b>claude mcp list</b> and look for Connected</div></div>
  <div class="check-row"><div class="rank-badge">02</div><div class="check-copy">Check the scope — local is only this project</div></div>
  <div class="check-row"><div class="rank-badge">03</div><div class="check-copy">Confirm the start command can actually run</div></div>
  <div class="check-row"><div class="rank-badge">04</div><div class="check-copy">Add the API key, or sign in with <b>/mcp</b></div></div>
  <div class="check-row"><div class="rank-badge">05</div><div class="check-copy">Look up last night's result before you install</div></div>
</div>
"""

TIP1 = """
<div class="eyebrow"><span class="dot"></span>CHECK 1 OF 5 · IN YOUR SHELL</div>
<h2>Run <em>claude mcp list</em>. Look for Connected.</h2>
<p class="sub">Adding the server only writes the config. The list is how you know Claude can actually talk to it.</p>
<div class="visual">
  <div class="cmd-card" style="flex:0 0 auto">
    <div class="cmd-kicker">In your shell</div>
    <div class="cmd-pill">claude mcp list</div>
  </div>
  <div class="status-row">
    <div class="status-mark">✔</div>
    <div>
      <div class="status-title">Connected</div>
      <div class="status-desc">You're good. Claude can see the server.</div>
    </div>
  </div>
  <div class="status-row neutral">
    <div class="status-mark">!</div>
    <div>
      <div class="status-title">Needs authentication</div>
      <div class="status-desc">Open /mcp in Claude Code and sign in.</div>
    </div>
  </div>
  <div class="status-row neutral">
    <div class="status-mark">✘</div>
    <div>
      <div class="status-title">Failed to connect</div>
      <div class="status-desc">It didn't start. The same line includes the error.</div>
    </div>
  </div>
</div>
<p class="note">In an open session, /mcp shows the same statuses and lets you reconnect.</p>
"""

TIP2 = """
<div class="eyebrow"><span class="dot"></span>CHECK 2 OF 5 · SCOPE</div>
<h2>Local scope is only <em>this project</em>.</h2>
<p class="sub">That's the default. Claude stores it in ~/.claude.json under that folder, so it won't appear if you open a different one.</p>
<div class="visual">
  <div class="check-row"><div class="scope-name">local</div><div class="check-copy">This project, just you. Default. Stored in ~/.claude.json</div></div>
  <div class="check-row"><div class="scope-name">project</div><div class="check-copy">This repo, shared with the team. Writes .mcp.json</div></div>
  <div class="check-row"><div class="scope-name">user</div><div class="check-copy">Every project on this machine. Also ~/.claude.json</div></div>
  <div class="cmd-card" style="flex:0 0 auto">
    <div class="cmd-kicker">Want it everywhere on this machine?</div>
    <div class="cmd-pill">claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic</div>
  </div>
</div>
<p class="note">If you added it in one repo and opened another, this is usually why it "disappeared."</p>
"""

TIP3 = """
<div class="eyebrow"><span class="dot"></span>CHECK 3 OF 5 · LOCAL SERVERS</div>
<h2>Make sure the start command can <em>actually run</em>.</h2>
<p class="sub">Most npm servers launch with npx. Node has to be installed, and the -- before the command is required so Claude Code doesn't swallow the server's flags.</p>
<div class="visual">
  <div class="cmd-card">
    <div class="cmd-kicker">Official stdio example</div>
    <div class="cmd-pill">claude mcp add --env AIRTABLE_API_KEY=YOUR_KEY --transport stdio airtable \\
  -- npx -y airtable-mcp-server</div>
  </div>
</div>
<p class="note">If list says Failed to connect the first time, wait for the package to finish fetching, then reconnect from /mcp. A cold npx -y download can outlast the connect timeout — we even pre-warm the npm cache in our nightly tests so we don't grade that as a fail.</p>
"""

TIP4 = """
<div class="eyebrow"><span class="dot"></span>CHECK 4 OF 5 · KEYS AND SIGN-IN</div>
<h2>Add the API key, or sign in with <em>/mcp</em>.</h2>
<p class="sub">A server that needs a key will sit there looking installed until you give it one.</p>
<div class="visual">
  <div class="check-row"><div class="rank-badge">01</div><div class="check-copy">Stdio: pass <b>--env KEY=value</b>. Put another option, like --transport stdio, between --env and the server name.</div></div>
  <div class="check-row"><div class="rank-badge">02</div><div class="check-copy">Remote / OAuth: type <b>/mcp</b> in Claude Code and complete sign-in.</div></div>
  <div class="check-row"><div class="rank-badge">03</div><div class="check-copy">Then choose Reconnect on that server in /mcp.</div></div>
  <div class="check-row"><div class="rank-badge">04</div><div class="check-copy">If a <b>${VAR}</b> is missing, <b>claude mcp list</b> warns about the variable.</div></div>
</div>
<p class="note">We see this every night in our tests: a lot of MCP servers need a key, and Connected is the line that tells you it's real.</p>
"""

TIP5 = """
<div class="eyebrow"><span class="dot"></span>CHECK 5 OF 5 · BEFORE YOU INSTALL</div>
<h2>Look up a <em>real install</em> first.</h2>
<p class="sub">Type the tool, pick Claude Code, and read last night's sandbox result. For MCP, a pass means claude mcp list said Connected.</p>
<div class="visual">
  <div class="cmd-card" style="flex:0 0 auto">
    <div class="cmd-kicker">Is it safe to install today?</div>
    <div class="cmd-pill">skillmaxx.gilventures.ai/reports/latest/</div>
  </div>
  <div class="cmd-kicker" style="margin:4px 0 0">The same idea applies in Cursor and Codex</div>
  <div class="check-row"><div class="scope-name">Cursor</div><div class="check-copy">The MCP list should say ready.</div></div>
  <div class="check-row"><div class="scope-name">Codex</div><div class="check-copy">The server should be listed as enabled.</div></div>
</div>
<p class="note">Two clean nights tell you more than a star count. Free, updated every night.</p>
"""

CTA = """
<div class="eyebrow"><span class="dot"></span>FREE WEEKLY NEWSLETTER</div>
<h2>Tips like these, plus what actually <em>installed</em>, every Sunday.</h2>
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

X_TIP_LIST = """
<div class="eyebrow"><span class="dot"></span>CHECK 1 OF 5 · IN YOUR SHELL</div>
<h2>Run <em>claude mcp list</em>. Look for Connected.</h2>
<p class="sub">Adding the server only writes the config. The list is how you know Claude can actually talk to it.</p>
<div class="visual">
  <div class="cmd-card" style="flex:0 0 auto">
    <div class="cmd-kicker">In your shell</div>
    <div class="cmd-pill">claude mcp list</div>
  </div>
  <div class="status-row">
    <div class="status-mark">✔</div>
    <div>
      <div class="status-title">Connected</div>
      <div class="status-desc">You're good. Claude can see the server.</div>
    </div>
  </div>
  <div class="status-row neutral">
    <div class="status-mark">!</div>
    <div>
      <div class="status-title">Needs authentication</div>
      <div class="status-desc">Open /mcp in Claude Code and sign in.</div>
    </div>
  </div>
  <div class="status-row neutral">
    <div class="status-mark">✘</div>
    <div>
      <div class="status-title">Failed to connect</div>
      <div class="status-desc">It didn't start. The same line includes the error.</div>
    </div>
  </div>
</div>
<p class="note">In an open session, /mcp shows the same statuses and lets you reconnect.</p>
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


def write_contact_sheet(pngs: list[Path], labels: list[str], dest: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    if not pngs:
        raise SystemExit("no pngs for contact sheet")
    cols = 4
    rows = (len(pngs) + cols - 1) // cols
    thumb = 360
    label_h = 36
    pad = 16
    bg = (10, 10, 11)
    sheet_w = pad + cols * (thumb + pad)
    sheet_h = pad + rows * (thumb + label_h + pad)
    sheet = Image.new("RGB", (sheet_w, sheet_h), bg)
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    for i, (src, label) in enumerate(zip(pngs, labels)):
        r, c = divmod(i, cols)
        x = pad + c * (thumb + pad)
        y = pad + r * (thumb + label_h + pad)
        im = Image.open(src).convert("RGB")
        im = im.resize((thumb, thumb), Image.Resampling.LANCZOS)
        sheet.paste(im, (x, y))
        im.close()
        draw.text((x, y + thumb + 8), label, fill=(229, 231, 235), font=font)
    dest.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest, "PNG")


def main() -> int:
    g.set_render(width=1080, height=1080, cta="newsletter")
    dest_root = ROOT / "src/assets/social/carousels/2026-11-23-claude-code-mcp-checks"
    li_dir = dest_root
    x_dir = dest_root / "x"

    li = pack([HOOK, TIP1, TIP2, TIP3, TIP4, TIP5, CTA], "CLAUDE CODE TIPS")
    xs = pack([X_HOOK, X_TIP_LIST, TIP5, X_CTA], "CLAUDE CODE TIPS")

    li_pngs = render_set(li, li_dir)
    x_pngs = render_set(xs, x_dir)
    pdf_path = dest_root / "carousel.pdf"
    write_pdf(li_pngs, pdf_path)
    labels = [f"LI {i+1:02d}" for i in range(len(li_pngs))] + [
        f"X {i+1:02d}" for i in range(len(x_pngs))
    ]
    contact = dest_root / "contact-sheet.png"
    write_contact_sheet(li_pngs + x_pngs, labels, contact)
    print(f"linkedin {len(li_pngs)} slides + {pdf_path.name} -> {li_dir}")
    print(f"x        {len(x_pngs)} slides -> {x_dir}")
    print(f"contact  {contact.relative_to(ROOT)}")
    for p in li_pngs + x_pngs + [pdf_path, contact]:
        print(f"  {p.relative_to(ROOT)}  {p.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
