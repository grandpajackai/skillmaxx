#!/usr/bin/env python3
"""Render the Nov 23 Claude Code MCP checks carousel as 1080x1350 PNGs.

One reader, one tool: a developer using Claude Code who installed an MCP
server and still cannot see it. Copy is grounded in official Anthropic
docs (code.claude.com/docs/en/mcp, plugins/install, skills) and in
src/how-we-test.njk (the npx cold-start note and the SkillMaxx lookup).
No scorecard-drop figures, and no SkillMaxx failure story.

Layouts come from the archetype library in generate.py so each slide is
a distinct frame (cover strip, terminal, scope tiers, split gotcha,
two-path flow, lookup card, full-bleed CTA). Default canvas is the v3
1080x1350 portrait size. Pass --animate to also write per-slide MP4s
and preview.mp4 (the Instagram / TikTok standard) under animated/.

Does not post or talk to Buffer.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

import generate as g  # noqa: E402

BADGE = "CLAUDE CODE TIPS"


# ---------------------------------------------------------------------------
# Slide bodies. Copy and claims stay exactly as reviewed / doc-verified.
# ---------------------------------------------------------------------------

def body_cover(animate: bool = False) -> str:
    strip = g.cover_check_strip(
        [
            {"num": "01", "html": "Run <b>claude mcp list</b> and look for Connected"},
            {"num": "02", "html": "Check the scope — local is only this project"},
            {"num": "03", "html": "Confirm the start command can actually run"},
            {"num": "04", "html": "Add the API key, or sign in with <b>/mcp</b>"},
            {"num": "05", "html": "Look up last night's result before you install"},
        ],
        animate=animate,
    )
    return f"""
<div class="eyebrow"><span class="dot"></span>CLAUDE CODE · MCP SERVERS</div>
<h1 style="font-size:64px">Your MCP is installed.<br><span style="white-space:nowrap">Claude Code still <em>can't see it</em>.</span></h1>
<p class="cover-sub">Check these 5 things before you tear the config apart.</p>
<div class="visual">{strip}</div>
"""


def body_check1(animate: bool = False) -> str:
    term = g.terminal_window(
        title="zsh  ·  claude mcp list",
        command="claude mcp list",
        lines=[
            {
                "kind": "ok",
                "mark": "✔",
                "title": "Connected",
                "desc": "You're good. Claude can see the server.",
            },
            {
                "kind": "auth",
                "mark": "!",
                "title": "Needs authentication",
                "desc": "Open /mcp in Claude Code and sign in.",
            },
            {
                "kind": "fail",
                "mark": "✘",
                "title": "Failed to connect",
                "desc": "It didn't start. The same line includes the error.",
            },
        ],
        animate=animate,
    )
    return f"""
<div class="eyebrow"><span class="dot"></span>CHECK 1 OF 5 · IN YOUR SHELL</div>
<h2>Run <em>claude mcp list</em>. Look for Connected.</h2>
<p class="sub">Adding the server only writes the config. The list is how you know Claude can actually talk to it.</p>
<div class="visual">{term}</div>
<p class="note">In an open session, /mcp shows the same statuses and lets you reconnect.</p>
"""


def body_check2(animate: bool = False) -> str:
    tiers = g.scope_tiers(
        [
            {
                "kind": "local",
                "name": "local",
                "copy": "This project, just you. Default. Stored in ~/.claude.json",
            },
            {
                "kind": "project",
                "name": "project",
                "copy": "This repo, shared with the team. Writes .mcp.json",
            },
            {
                "kind": "user",
                "name": "user",
                "copy": "Every project on this machine. Also ~/.claude.json",
            },
        ],
        animate=animate,
    )
    cmd = g.command_card(
        kicker="Want it everywhere on this machine?",
        command="claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic",
        animate=animate,
        delay=0.72,
    )
    return f"""
<div class="eyebrow"><span class="dot"></span>CHECK 2 OF 5 · SCOPE</div>
<h2>Local scope is only <em>this project</em>.</h2>
<p class="sub">That's the default. Claude stores it in ~/.claude.json under that folder, so it won't appear if you open a different one.</p>
<div class="visual">{tiers}{cmd}</div>
<p class="note">If you added it in one repo and opened another, this is usually why it "disappeared."</p>
"""


def body_check3(animate: bool = False) -> str:
    cmd = g.command_card(
        kicker="Official stdio example",
        command="claude mcp add --env AIRTABLE_API_KEY=YOUR_KEY --transport stdio airtable \\\n  -- npx -y airtable-mcp-server",
        animate=animate,
        delay=0.20,
    )
    # The gotcha sentence is the documented human touch from how-we-test.
    # Surrounding sentences stay in the callout body, claims unchanged.
    gotcha = g.gotcha_callout(
        kicker="The real gotcha",
        headline="A cold npx -y download can outlast the connect timeout",
        body=(
            "If list says Failed to connect the first time, wait for the package "
            "to finish fetching, then reconnect from /mcp. We even pre-warm the "
            "npm cache in our nightly tests so we don't grade that as a fail."
        ),
        animate=animate,
        delay=0.55,
    )
    return f"""
<div class="eyebrow"><span class="dot"></span>CHECK 3 OF 5 · LOCAL SERVERS</div>
<h2>Make sure the start command can <em>actually run</em>.</h2>
<p class="sub">Most npm servers launch with npx. Node has to be installed, and the -- before the command is required so Claude Code doesn't swallow the server's flags.</p>
<div class="visual split-gotcha">{cmd}{gotcha}</div>
"""


def body_check4(animate: bool = False) -> str:
    flow = g.two_path_flow(
        left_kicker="Stdio",
        left_html="Pass <b>--env KEY=value</b>. Put another option, like --transport stdio, between --env and the server name.",
        right_kicker="Remote / OAuth",
        right_html="Type <b>/mcp</b> in Claude Code and complete sign-in.",
        after=[
            "Then choose Reconnect on that server in /mcp.",
            "If a <b>${VAR}</b> is missing, <b>claude mcp list</b> warns about the variable.",
        ],
        animate=animate,
    )
    return f"""
<div class="eyebrow"><span class="dot"></span>CHECK 4 OF 5 · KEYS AND SIGN-IN</div>
<h2>Add the API key, or sign in with <em>/mcp</em>.</h2>
<p class="sub">A server that needs a key will sit there looking installed until you give it one.</p>
<div class="visual">{flow}</div>
<p class="note">We see this every night in our tests: a lot of MCP servers need a key, and Connected is the line that tells you it's real.</p>
"""


def body_check5(animate: bool = False) -> str:
    card = g.lookup_result_card(
        kicker="Is it safe to install today?",
        url="skillmaxx.gilventures.ai/reports/latest/",
        badge_label="Last night's result",
        badge_note="Illustrative layout — no live figure on this slide.",
        chips_kicker="The same idea applies in Cursor and Codex",
        chips=[
            {"name": "Cursor", "copy": "The MCP list should say ready."},
            {"name": "Codex", "copy": "The server should be listed as enabled."},
        ],
        animate=animate,
    )
    return f"""
<div class="eyebrow"><span class="dot"></span>CHECK 5 OF 5 · BEFORE YOU INSTALL</div>
<h2>Look up a <em>real install</em> first.</h2>
<p class="sub">Type the tool, pick Claude Code, and read last night's sandbox result. For MCP, a pass means claude mcp list said Connected.</p>
<div class="visual">{card}</div>
<p class="note">Two clean nights tell you more than a star count. Free, updated every night.</p>
"""


def body_cta(animate: bool = False) -> str:
    panel = g.cta_bleed_panel(
        kicker="",
        title_html="Subscribe free",
        url="skillmaxx.gilventures.ai/newsletter/",
        tagline="No hype. Just what works.",
        desc="Also the daily report and per-agent matrix, at the same site, $0.",
        animate=animate,
    )
    return f"""
<div class="eyebrow"><span class="dot"></span>FREE WEEKLY NEWSLETTER</div>
<h2>Tips like these, plus what actually <em>installed</em>, every Sunday.</h2>
<p class="sub">The free SkillMaxx newsletter is the weekly scorecard and the useful context around it.</p>
<div class="visual cta-bleed">{panel}</div>
"""


# LinkedIn (7) and X (4: cover, check 1 terminal, check 5, CTA)
LI_SPEC = [
    # body, bg, motif, next_label, duration
    (body_cover, "a", None, "Check 1 — claude mcp list", 6.0),
    (body_check1, "b", "01", "Check 2 — scope", 5.8),
    (body_check2, "c", "02", "Check 3 — start command", 5.8),
    (body_check3, "d", "03", "Check 4 — key or /mcp", 6.0),
    (body_check4, "e", "04", "Check 5 — last night's result", 5.8),
    (body_check5, "f", "05", "Subscribe free", 5.6),
    (body_cta, "cta", None, None, 5.4),
]

X_SPEC = [
    LI_SPEC[0],
    LI_SPEC[1],
    LI_SPEC[5],
    LI_SPEC[6],
]


def pack(spec: list, badge: str, animate: bool = False) -> list[str]:
    total = len(spec)
    out = []
    for i, (fn, bg, motif, nxt, dur) in enumerate(spec, 1):
        out.append(
            g.wrap_archetype_slide(
                fn(animate=animate),
                i,
                total,
                badge,
                animate=animate,
                duration=dur,
                bg=bg,
                motif=motif,
                next_label=nxt,
            )
        )
    return out


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
    # 4:5 thumbs for the 1080x1350 canvas
    thumb_w, thumb_h = 360, 450
    label_h = 36
    pad = 16
    bg = (10, 10, 11)
    sheet_w = pad + cols * (thumb_w + pad)
    sheet_h = pad + rows * (thumb_h + label_h + pad)
    sheet = Image.new("RGB", (sheet_w, sheet_h), bg)
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    for i, (src, label) in enumerate(zip(pngs, labels)):
        r, c = divmod(i, cols)
        x = pad + c * (thumb_w + pad)
        y = pad + r * (thumb_h + label_h + pad)
        im = Image.open(src).convert("RGB")
        im = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(im, (x, y))
        im.close()
        draw.text((x, y + thumb_h + 8), label, fill=(229, 231, 235), font=font)
    dest.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest, "PNG")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--animate",
        action="store_true",
        help="Also render per-slide MP4s + preview.mp4 under animated/ (Instagram / TikTok standard).",
    )
    parser.add_argument("--fps", type=int, default=30)
    args = parser.parse_args(argv)

    g.set_render(width=1080, height=1350, cta="newsletter")
    dest_root = ROOT / "src/assets/social/carousels/2026-11-23-claude-code-mcp-checks"
    li_dir = dest_root
    x_dir = dest_root / "x"
    anim_dir = dest_root / "animated"

    li = pack(LI_SPEC, BADGE, animate=False)
    xs = pack(X_SPEC, BADGE, animate=False)

    li_pngs = g.render_slides_html(li, li_dir)
    x_pngs = g.render_slides_html(xs, x_dir)
    pdf_path = dest_root / "carousel.pdf"
    write_pdf(li_pngs, pdf_path)
    labels = [f"LI {i+1:02d}" for i in range(len(li_pngs))] + [
        f"X {i+1:02d}" for i in range(len(x_pngs))
    ]
    contact = dest_root / "contact-sheet.png"
    write_contact_sheet(li_pngs + x_pngs, labels, contact)
    print(f"linkedin {len(li_pngs)} slides + {pdf_path.name} -> {li_dir}  (1080x1350)")
    print(f"x        {len(x_pngs)} slides -> {x_dir}")
    print(f"contact  {contact.relative_to(ROOT)}")

    if args.animate:
        li_anim = pack(LI_SPEC, BADGE, animate=True)
        mp4s, anim_pngs, preview, durs = g.render_slides_animated(li_anim, anim_dir, fps=args.fps)
        print(f"animated {len(mp4s)} mp4s + {preview.name} -> {anim_dir}")
        for p, d in zip(mp4s, durs):
            print(f"  {p.relative_to(ROOT)}  {p.stat().st_size} bytes  {d:.2f}s")
        print(f"  {preview.relative_to(ROOT)}  {preview.stat().st_size} bytes")
        for p in anim_pngs:
            print(f"  {p.relative_to(ROOT)}  {p.stat().st_size} bytes")

    for p in li_pngs + x_pngs + [pdf_path, contact]:
        print(f"  {p.relative_to(ROOT)}  {p.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
