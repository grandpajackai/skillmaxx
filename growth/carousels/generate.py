#!/usr/bin/env python3
"""Free, local 1080x1350 PNG carousel generator for SkillMaxx (news + leaderboard).

Reads only real committed nightly data (src/_data/reports.json, weeks.json, latestRows.json,
data/skills.json, data/meta/meta.json) and renders HTML/CSS slides with bundled Inter & JetBrains Mono
fonts via headless Chromium (Python playwright, falling back to google-chrome/chromium CLI).

Usage:
  python3 growth/carousels/generate.py [--format news|leaderboard|all] [--date YYYY-MM-DD] [--out DIR] [--zip]
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
AG_NAME = {
    "claude_code": "Claude Code",
    "grok_build": "Grok Build",
    "codex": "Codex",
    "cursor": "Cursor",
    "pi": "Pi",
}
AG_SHORT = {
    "claude_code": "Claude",
    "grok_build": "Grok",
    "codex": "Codex",
    "cursor": "Cursor",
    "pi": "Pi",
}
AG_COLOR = {
    "claude_code": "#F59E0B",
    "grok_build": "#22D3EE",
    "codex": "#22C55E",
    "cursor": "#A78BFA",
    "pi": "#F472B6",
}
CAT_MERGE = {
    "developer tools": "development",
    "observability": "monitoring",
    "mcp (npm)": "mcp servers",
    "learning": "education & research",
    "scientific research": "education & research",
    "data & analytics": "database",
    "files": "utilities",
    "memory": "utilities",
    "reasoning": "utilities",
    "web": "utilities",
    "creativity": "design",
    "migration": "development",
    "location": "other",
    "math": "other",
    "finance": "other",
    "business & operations": "productivity",
    "testing": "development",
}
TYPE_LABEL = {
    "plugin": "Plugin",
    "mcp-server": "MCP",
    "npm-mcp-package": "MCP npm",
    "skill": "Skill",
}


def rd_json(rel: str, default=None):
    p = ROOT / rel
    if not p.is_file():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def fmt_date(iso_str: str) -> str:
    d = date.fromisoformat(iso_str[:10])
    return f"{d.strftime('%b')} {d.day}, {d.year}"


def fmt_short(iso_str: str) -> str:
    d = date.fromisoformat(iso_str[:10])
    return f"{d.strftime('%b')} {d.day}"


def fmt_stars(n: int | None) -> str:
    if not n:
        return ""
    if n >= 1000:
        return f"{n/1000:.1f}k ★"
    return f"{n} ★"


def esc(s) -> str:
    return html.escape(str(s or ""))


def load_data(target_date: str | None = None) -> dict:
    reps = sorted(rd_json("src/_data/reports.json", []), key=lambda r: r["date"], reverse=True)
    if not reps:
        raise SystemExit("No reports in src/_data/reports.json")
    rep = next((r for r in reps if r["date"] == target_date), reps[0]) if target_date else reps[0]
    weeks = sorted(rd_json("src/_data/weeks.json", []), key=lambda w: w["key"], reverse=True)
    wk = next((w for w in weeks if w.get("start", "") <= rep["date"] <= w.get("end", "")), weeks[0])
    latest_rows = rd_json("src/_data/latestRows.json", {})
    skills_raw = rd_json("data/skills.json", {}).get("items") or []
    meta = rd_json("data/meta/meta.json", {})
    skills = {}
    for sk in skills_raw:
        m = dict(meta.get(sk["slug"]) or {})
        repo = m.get("repo") or ""
        if any(x in repo for x in ("anthropics/claude-plugins-", "openai/plugins", "xai-org/plugin-marketplace")):
            m["stars"] = None
        cat_raw = (sk.get("category") or "other").lower()
        cat = CAT_MERGE.get(cat_raw, cat_raw)
        skills[sk["slug"]] = {**sk, "stars": m.get("stars"), "cat_norm": cat}
    return {
        "rep": rep,
        "reps": reps,
        "wk": wk,
        "latest_rows": latest_rows,
        "skills": skills,
    }


def font_css() -> str:
    def b64(rel: str) -> str:
        return base64.b64encode((ROOT / rel).read_bytes()).decode("ascii")

    inter = b64("src/assets/fonts/inter.woff2")
    jbm4 = b64("src/assets/fonts/jetbrains-mono-latin-400-normal.woff2")
    jbm5 = b64("src/assets/fonts/jetbrains-mono-latin-500-normal.woff2")
    return f"""
@font-face {{ font-family: 'Inter'; font-weight: 100 900; src: url(data:font/woff2;base64,{inter}) format('woff2'); }}
@font-face {{ font-family: 'JetBrains Mono'; font-weight: 400; src: url(data:font/woff2;base64,{jbm4}) format('woff2'); }}
@font-face {{ font-family: 'JetBrains Mono'; font-weight: 500 700; src: url(data:font/woff2;base64,{jbm5}) format('woff2'); }}
"""


def brand_mark(size: int = 44) -> str:
    svg = (ROOT / "growth/brand/b-mark.svg").read_text(encoding="utf-8")
    return svg.replace("<svg ", f'<svg width="{size}" height="{size}" style="display:block;flex:none" ')


BASE_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  width: 1080px;
  height: 1350px;
  overflow: hidden;
  background: #0A0A0B;
  color: #EDEDEF;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  -webkit-font-smoothing: antialiased;
}
.slide {
  position: relative;
  width: 1080px;
  height: 1350px;
  padding: 64px 72px 58px;
  display: flex;
  flex-direction: column;
  background:
    radial-gradient(640px 420px at 92% 4%, rgba(198,244,50,0.16), transparent 65%),
    radial-gradient(520px 360px at 8% 96%, rgba(34,211,238,0.08), transparent 65%),
    #0A0A0B;
}
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 44px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.02em;
}
.brand span { color: #C6F432; }
.top-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}
.tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #C6F432;
  background: rgba(198,244,50,0.10);
  border: 1px solid rgba(198,244,50,0.32);
  padding: 8px 16px;
  border-radius: 99px;
}
.page-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 17px;
  color: #8A8F98;
  background: #131316;
  border: 1px solid rgba(255,255,255,0.10);
  padding: 8px 16px;
  border-radius: 99px;
}
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  align-self: flex-start;
  font-family: 'JetBrains Mono', monospace;
  font-size: 17px;
  color: #EDEDEF;
  background: #141418;
  border: 1px solid rgba(255,255,255,0.14);
  padding: 9px 18px;
  border-radius: 99px;
  margin-bottom: 28px;
}
.dot { width: 10px; height: 10px; border-radius: 50%; background: #C6F432; box-shadow: 0 0 12px #C6F432; }
h1 {
  font-size: 74px;
  line-height: 1.05;
  font-weight: 800;
  letter-spacing: -0.035em;
  margin-bottom: 24px;
}
h1 em { font-style: normal; color: #C6F432; }
h2 {
  font-size: 50px;
  line-height: 1.1;
  font-weight: 700;
  letter-spacing: -0.03em;
  margin-bottom: 12px;
}
.sub {
  font-size: 25px;
  line-height: 1.42;
  color: #9CA3AF;
  margin-bottom: 34px;
}
.cover-sub {
  font-size: 29px;
  line-height: 1.45;
  color: #A1A1AA;
  margin-bottom: 46px;
}
.stat-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
  margin-top: auto;
  margin-bottom: 28px;
}
.stat-card {
  background: #121215;
  border: 1px solid rgba(255,255,255,0.11);
  border-radius: 22px;
  padding: 28px 26px;
}
.stat-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 52px;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: #EDEDEF;
  margin-bottom: 8px;
}
.stat-val.lime { color: #C6F432; }
.stat-lbl { font-size: 19px; color: #8A8F98; line-height: 1.3; }
.card-stack { display: flex; flex-direction: column; gap: 16px; }
.card {
  background: #121215;
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 20px;
  padding: 22px 26px;
}
.bar-row {
  background: #121215;
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 20px;
  padding: 22px 26px;
}
.bar-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 14px;
}
.bar-name { font-size: 26px; font-weight: 600; display: flex; align-items: center; gap: 12px; }
.bar-nums { font-family: 'JetBrains Mono', monospace; font-size: 24px; font-weight: 600; }
.bar-nums span { color: #8A8F98; font-size: 19px; font-weight: 400; margin-left: 8px; }
.track { height: 18px; background: #1E1E24; border-radius: 99px; overflow: hidden; }
.fill { height: 100%; border-radius: 99px; background: #C6F432; }
.pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 15px;
  padding: 5px 12px;
  border-radius: 99px;
  border: 1px solid rgba(255,255,255,0.14);
  color: #D4D4D8;
  background: #18181D;
}
.pill.lime { color: #C6F432; border-color: rgba(198,244,50,0.38); background: rgba(198,244,50,0.08); }
.pill.red { color: #FCA5A5; border-color: rgba(239,68,68,0.40); background: rgba(239,68,68,0.10); }
.pill.amber { color: #FCD34D; border-color: rgba(245,158,11,0.40); background: rgba(245,158,11,0.10); }
.pill.green { color: #86EFAC; border-color: rgba(34,197,94,0.38); background: rgba(34,197,94,0.10); }
.pill.cyan { color: #67E8F9; border-color: rgba(34,211,238,0.38); background: rgba(34,211,238,0.09); }
.item-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  background: #121215;
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 20px;
  padding: 20px 24px;
}
.item-title { font-size: 25px; font-weight: 600; color: #EDEDEF; margin-bottom: 6px; }
.item-desc { font-size: 18px; color: #9CA3AF; line-height: 1.35; }
.rank-badge {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: rgba(198,244,50,0.12);
  border: 1px solid rgba(198,244,50,0.32);
  color: #C6F432;
  font-family: 'JetBrains Mono', monospace;
  font-size: 22px;
  font-weight: 700;
  display: grid;
  place-items: center;
  flex: none;
}
.note {
  margin-top: auto;
  padding-top: 18px;
  font-size: 18px;
  color: #8A8F98;
  line-height: 1.4;
}
.cta-box {
  background: linear-gradient(180deg, #17181C, #111114);
  border: 1px solid rgba(198,244,50,0.35);
  border-radius: 24px;
  padding: 34px 36px;
  margin-bottom: 22px;
}
.cta-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #C6F432;
  margin-bottom: 10px;
}
.cta-url {
  font-family: 'JetBrains Mono', monospace;
  font-size: 28px;
  font-weight: 600;
  color: #EDEDEF;
  margin-bottom: 10px;
  word-break: break-all;
}
.cta-desc { font-size: 21px; color: #9CA3AF; line-height: 1.4; }
.footer {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid rgba(255,255,255,0.10);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: 'JetBrains Mono', monospace;
  font-size: 17px;
  color: #71717A;
}
.footer b { color: #D4D4D8; font-weight: 500; }
"""


def wrap_slide(body: str, idx: int, total: int, badge: str, footer_right: str = "Swipe →") -> str:
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><style>{font_css()}{BASE_CSS}</style></head>
<body>
  <div class="slide">
    <div class="topbar">
      <div class="brand">{brand_mark(46)}<div>Skill<span>Maxx</span></div></div>
      <div class="top-meta">
        <div class="tag">{esc(badge)}</div>
        <div class="page-num">{idx:02d} / {total:02d}</div>
      </div>
    </div>
    <div class="content">{body}</div>
    <div class="footer">
      <div><b>skillmaxx.gilventures.ai</b> · 5 agents · $0 free directory</div>
      <div>{esc(footer_right)}</div>
    </div>
  </div>
</body></html>"""


def build_news_slides(data: dict) -> list[str]:
    rep, wk, skills = data["rep"], data["wk"], data["skills"]
    d_lbl = fmt_date(rep["date"])
    tested = rep.get("tested") or rep["total"]
    rate = round(100 * rep["pass"] / tested, 1) if tested else 0
    total_slides = 6

    # Slide 1: Cover
    s1 = f"""
    <div class="eyebrow"><span class="dot"></span>NIGHTLY INSTALL REPORT · {esc(d_lbl.upper())}</div>
    <h1><em>{rep['pass']:,}</em> of {tested:,} agent add-on installs passed.</h1>
    <p class="cover-sub">Real sandboxed installs across {rep.get('addons', len(skills)):,} skills, plugins, and MCP servers in Claude Code, Codex, Grok Build, Cursor, and Pi.</p>
    <div class="card" style="margin-bottom:24px;border-color:rgba(198,244,50,0.28);background:rgba(198,244,50,0.05)">
      <div style="font-size:21px;color:#EDEDEF;line-height:1.45">
        <b style="color:#C6F432">No marketing claims — just logs.</b> Every add-on is re-installed in a fresh container with no API keys, and failures stay visible.
      </div>
    </div>
    <div class="stat-grid">
      <div class="stat-card"><div class="stat-val lime">{rate}%</div><div class="stat-lbl">Clean install rate<br>(judgeable)</div></div>
      <div class="stat-card"><div class="stat-val">{rep.get('addons', len(skills)):,}</div><div class="stat-lbl">Add-ons tested<br>across 5 agents</div></div>
      <div class="stat-card"><div class="stat-val">{rep.get('needs_key', 0)}</div><div class="stat-lbl">Skipped for<br>API key needed</div></div>
    </div>
    """

    # Slide 2: By Agent
    by_rows = []
    for ag, v in (rep.get("by") or {}).items():
        judge = (v.get("total") or 0) - (v.get("needs_key") or 0)
        if judge > 0:
            by_rows.append((v.get("pass", 0) / judge, ag, v.get("pass", 0), judge, v.get("broken", 0)))
    by_rows.sort(reverse=True)
    bars = []
    for r, ag, ps, j, br in by_rows:
        pct = round(r * 100, 1)
        c = AG_COLOR.get(ag, "#C6F432")
        bars.append(f"""
        <div class="bar-row">
          <div class="bar-head">
            <div class="bar-name"><span style="width:14px;height:14px;border-radius:50%;background:{c};display:inline-block"></span>{esc(AG_NAME.get(ag, ag))}</div>
            <div class="bar-nums">{pct}% <span>{ps}/{j} clean</span></div>
          </div>
          <div class="track"><div class="fill" style="width:{pct}%;background:{c}"></div></div>
        </div>""")
    s2 = f"""
    <h2>Pass rate by coding agent</h2>
    <p class="sub">Judgeable installs on {esc(d_lbl)} (5 installs per agent require an API key and are excluded).</p>
    <div class="card-stack">{''.join(bars)}</div>
    <p class="note">Each agent is tested only on the add-on formats it supports (Claude Code &amp; Grok Build run plugins + MCP; Cursor runs MCP; Codex &amp; Pi run skills + MCP).</p>
    """

    # Slide 3: Week Trend
    trend = wk.get("trend") or []
    t_cards = []
    for t in trend[-5:]:
        t_cards.append(f"""
        <div class="bar-row">
          <div class="bar-head">
            <div class="bar-name">{esc(fmt_date(t['date']))}</div>
            <div class="bar-nums">{t['rate']}% <span>{t['pass']:,} / {t['tested']:,}</span></div>
          </div>
          <div class="track"><div class="fill" style="width:{t['rate']}%"></div></div>
        </div>""")
    s3 = f"""
    <h2>Week {esc(wk['key'])} trend</h2>
    <p class="sub">{wk.get('runs', len(trend))} nightly sandbox runs from {esc(fmt_short(wk['first']))} to {esc(fmt_short(wk['last']))}.</p>
    <div class="card-stack">{''.join(t_cards)}</div>
    <div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:26px">
      <span class="pill green">Fixed: {wk.get('fixed_n', 0)}</span>
      <span class="pill red">Confirmed broke (2+ nights): {wk.get('broke_n', 0)}</span>
      <span class="pill amber">Flaky (flip-flopped): {wk.get('flaky_n', 0)}</span>
    </div>
    <p class="note">An add-on is only marked "broke" after failing two consecutive nights — one-night network timeouts are isolated as flaky.</p>
    """

    # Slide 4: What Broke & Flaky
    broke_map = defaultdict(list)
    for b in (rep.get("broke") or []) + (wk.get("broke") or []):
        slug = b.get("slug")
        if slug:
            ag = AG_SHORT.get(b.get("agent"), "")
            if ag and ag not in broke_map[slug]:
                broke_map[slug].append(ag)
            elif slug not in broke_map:
                broke_map[slug] = []
    # Keep distinct names
    name_of = {b["slug"]: b["name"] for b in (rep.get("broke") or []) + (wk.get("broke") or []) + (rep.get("flaky_list") or []) + (wk.get("flaky") or []) if b.get("slug")}
    broke_cards = []
    for slug, ags in list(broke_map.items())[:4]:
        ag_txt = f"Failed in: {', '.join(ags)}" if ags else "Failed 2+ nights running this week"
        broke_cards.append(f"""
        <div class="item-row" style="border-color:rgba(239,68,68,0.30)">
          <div>
            <div class="item-title">{esc(name_of.get(slug, slug))}</div>
            <div class="item-desc">{esc(ag_txt)}</div>
          </div>
          <span class="pill red">BROKE</span>
        </div>""")
    flaky_seen = []
    for fl in (rep.get("flaky_list") or []) + (wk.get("flaky") or []):
        sl = fl.get("slug")
        if sl and sl not in broke_map and sl not in flaky_seen:
            flaky_seen.append(sl)
    flaky_chips = " · ".join(esc(name_of.get(sl, sl)) for sl in flaky_seen[:4])
    s4 = f"""
    <h2>What broke this week</h2>
    <p class="sub">Confirmed two-night failures on {esc(d_lbl)} &amp; week {esc(wk['key'])}.</p>
    <div class="card-stack">{''.join(broke_cards) if broke_cards else '<div class="card"><div class="item-title">Zero new confirmed breaks tonight</div></div>'}</div>
    <div class="card" style="margin-top:24px;border-color:rgba(245,158,11,0.32)">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">
        <div style="font-size:22px;font-weight:600;color:#FCD34D">Flaky watchlist ({wk.get('flaky_n', len(flaky_seen))} add-ons)</div>
        <span class="pill amber">RETRYABLE</span>
      </div>
      <div class="item-desc" style="font-size:20px">{flaky_chips or 'None this week'}</div>
    </div>
    <p class="note">Full failure logs and exit codes are published on every add-on's page.</p>
    """

    # Slide 5: Fixed, Standout & New Additions
    standout = wk.get("standout") or rep.get("standout") or {}
    fixed_items = (rep.get("fixed") or []) + (wk.get("fixed") or [])
    seen_fix = set()
    fix_list = []
    for fx in fixed_items:
        if fx.get("slug") and fx["slug"] not in seen_fix:
            seen_fix.add(fx["slug"])
            fix_list.append(fx)
    recent_added = []
    for r in data["reps"][:7]:
        for ad in r.get("added") or []:
            recent_added.append((r["date"], ad))
    s5_cards = []
    if standout.get("slug"):
        s5_cards.append(f"""
        <div class="card" style="border-color:rgba(198,244,50,0.36);background:linear-gradient(180deg,rgba(198,244,50,0.06),#121215)">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">
            <span class="pill lime">WEEK STANDOUT · 5/5 AGENTS</span>
            <span class="pill">{esc(fmt_stars(standout.get('stars')) or 'Zero flakes')}</span>
          </div>
          <div class="item-title" style="font-size:30px">{esc(standout['name'])}</div>
          <div class="item-desc" style="font-size:20px">{esc(standout.get('desc') or 'Installed cleanly in all 5 agents all week.')}</div>
        </div>""")
    for fx in fix_list[:2]:
        s5_cards.append(f"""
        <div class="item-row" style="border-color:rgba(34,197,94,0.30)">
          <div>
            <div class="item-title">{esc(fx['name'])}</div>
            <div class="item-desc">Recovered after earlier failures</div>
          </div>
          <span class="pill green">FIXED</span>
        </div>""")
    for dt_s, ad in recent_added[:2]:
        s5_cards.append(f"""
        <div class="item-row" style="border-color:rgba(34,211,238,0.30)">
          <div>
            <div class="item-title">{esc(ad.get('name', ad.get('slug')))}</div>
            <div class="item-desc">Newly added to nightly suite ({esc(fmt_short(dt_s))})</div>
          </div>
          <span class="pill cyan">NEW TEST</span>
        </div>""")
    s5 = f"""
    <h2>Standout &amp; newly working</h2>
    <p class="sub">Zero-flake winners, recoveries, and recent additions tested in clean sandboxes.</p>
    <div class="card-stack">{''.join(s5_cards)}</div>
    <p class="note">Every tool page shows the last 10 nightly results per agent plus exact copy-paste install commands.</p>
    """

    # Slide 6: CTA
    s6 = f"""
    <div class="eyebrow"><span class="dot"></span>FREE · OPEN LOGS · UPDATED AT 2 AM ET</div>
    <h1>Check your tools <em>before</em> you install.</h1>
    <p class="cover-sub" style="margin-bottom:36px">Skip broken packages and guesswork across Claude Code, Codex, Grok Build, Cursor, and Pi.</p>
    <div class="cta-box">
      <div class="cta-label">Live Daily Install Reports</div>
      <div class="cta-url">skillmaxx.gilventures.ai/reports/latest/</div>
      <div class="cta-desc">Full pass/fail matrix, exact install commands, and sandbox log excerpts for every add-on.</div>
    </div>
    <div class="cta-box" style="border-color:rgba(34,211,238,0.35)">
      <div class="cta-label" style="color:#22D3EE">Free Weekly Newsletter</div>
      <div class="cta-url">skillmaxx.gilventures.ai/newsletter/</div>
      <div class="cta-desc">One short weekly digest: what passed, what broke, and what changed across all 5 agents.</div>
    </div>
    """

    slides = [s1, s2, s3, s4, s5, s6]
    return [
        wrap_slide(body, i + 1, total_slides, f"NIGHTLY REPORT · {fmt_short(rep['date']).upper()}", "Swipe →" if i < total_slides - 1 else "skillmaxx.gilventures.ai")
        for i, body in enumerate(slides)
    ]


def build_leaderboard_slides(data: dict) -> list[str]:
    rep, wk, skills, lr = data["rep"], data["wk"], data["skills"], data["latest_rows"]
    rows = lr.get("rows") or []
    d_lbl = fmt_date(rep["date"])
    total_slides = 6

    # Group latestRows by slug
    by_s: dict[str, dict[str, str]] = defaultdict(dict)
    names: dict[str, str] = {}
    for r in rows:
        by_s[r["s"]][r["a"]] = r["st"]
        names[r["s"]] = r["n"]

    five = []
    four = []
    cat_pass: Counter = Counter()
    for s, ags in by_s.items():
        passed = [a for a, st in ags.items() if st == "pass"]
        sk = skills.get(s, {})
        stars = sk.get("stars") or 0
        kind = TYPE_LABEL.get(sk.get("type", ""), "Tool")
        cat = sk.get("cat_norm", "other")
        if passed:
            cat_pass[cat] += 1
        entry = (stars, len(passed), s, names[s], kind, passed, sk.get("description") or "")
        if len(passed) == 5:
            five.append(entry)
        elif len(passed) == 4:
            four.append(entry)
    five.sort(key=lambda x: (-x[0], x[3].lower()))
    four.sort(key=lambda x: (-x[0], x[3].lower()))

    # Slide 1: Cover
    s1 = f"""
    <div class="eyebrow"><span class="dot"></span>WEEK {esc(wk['key'])} LEADERBOARD · {rep.get('addons', len(skills)):,} ADD-ONS</div>
    <h1>Top agent skills &amp; MCP servers that <em>actually</em> install.</h1>
    <p class="cover-sub">Ranked strictly from {wk.get('runs', 1)} nights of real sandbox installs — zero paid placements, zero self-reported claims.</p>
    <div style="display:flex;flex-wrap:wrap;gap:12px;margin-bottom:36px">
      {''.join(f'<span class="pill" style="font-size:18px;padding:10px 18px"><span style="width:10px;height:10px;border-radius:50%;background:{AG_COLOR[a]};display:inline-block"></span>{esc(AG_NAME[a])}</span>' for a in ("claude_code","grok_build","codex","cursor","pi"))}
    </div>
    <div class="stat-grid">
      <div class="stat-card"><div class="stat-val lime">{len(five)}</div><div class="stat-lbl">Pass in all<br>5 / 5 agents</div></div>
      <div class="stat-card"><div class="stat-val">{len(four)}</div><div class="stat-lbl">Pass in<br>4 / 5 agents</div></div>
      <div class="stat-card"><div class="stat-val">{rep['pass']:,}</div><div class="stat-lbl">Clean installs<br>on {esc(fmt_short(rep['date']))}</div></div>
    </div>
    """

    # Slide 2: Top 5/5 Universal
    five_cards = []
    for idx, (stars, _, sl, nm, kind, _, desc) in enumerate(five[:5], 1):
        st_pill = f'<span class="pill">{esc(fmt_stars(stars))}</span>' if stars else ""
        five_cards.append(f"""
        <div class="item-row">
          <div style="display:flex;align-items:center;gap:18px;min-width:0;flex:1">
            <div class="rank-badge">#{idx}</div>
            <div style="min-width:0">
              <div class="item-title" style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{esc(nm)}</div>
              <div class="item-desc" style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{esc(desc[:78]) if desc else 'Clean install in all 5 agents'}</div>
            </div>
          </div>
          <div style="display:flex;gap:8px;flex:none">
            {st_pill}
            <span class="pill green">5 / 5</span>
          </div>
        </div>""")
    s2 = f"""
    <h2>5-of-5 universal winners</h2>
    <p class="sub">{len(five)} add-ons installed cleanly across all 5 agents on {esc(d_lbl)} (ranked by GitHub stars).</p>
    <div class="card-stack">{''.join(five_cards)}</div>
    <p class="note">Universal MCP servers lead 5/5 compatibility because Claude Code, Codex, Grok Build, Cursor, and Pi all speak MCP.</p>
    """

    # Slide 3: Top 4/5 Cross-Agent Skills & Plugins
    four_cards = []
    for idx, (stars, _, sl, nm, kind, passed, desc) in enumerate(four[:5], 1):
        ag_tx = " · ".join(AG_SHORT.get(a, a) for a in passed)
        st_pill = f'<span class="pill">{esc(fmt_stars(stars))}</span>' if stars else f'<span class="pill">{esc(kind)}</span>'
        four_cards.append(f"""
        <div class="item-row">
          <div style="display:flex;align-items:center;gap:18px;min-width:0;flex:1">
            <div class="rank-badge" style="background:rgba(34,211,238,0.12);border-color:rgba(34,211,238,0.34);color:#22D3EE">#{idx}</div>
            <div style="min-width:0">
              <div class="item-title" style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{esc(nm)}</div>
              <div class="item-desc">{esc(ag_tx)}</div>
            </div>
          </div>
          <div style="display:flex;gap:8px;flex:none">
            {st_pill}
            <span class="pill cyan">4 / 5</span>
          </div>
        </div>""")
    s3 = f"""
    <h2>Top 4-of-5 cross-agent picks</h2>
    <p class="sub">Skills &amp; plugins passing in 4 agents on {esc(d_lbl)} (typically everything except MCP-only Cursor).</p>
    <div class="card-stack">{''.join(four_cards)}</div>
    <p class="note">See exact install commands per agent at skillmaxx.gilventures.ai/works-in/&lt;agent&gt;/.</p>
    """

    # Slide 4: Weekly Agent Reliability Scorecard
    rank_rows = []
    for idx, r in enumerate((wk.get("ranking") or [])[:5], 1):
        ag = r["agent"]
        c = AG_COLOR.get(ag, "#C6F432")
        rank_rows.append(f"""
        <div class="bar-row">
          <div class="bar-head">
            <div class="bar-name"><span style="color:#8A8F98;font-family:'JetBrains Mono',monospace;font-size:21px">#{idx}</span>{esc(r['name'])}</div>
            <div class="bar-nums">{r['rate']}% <span>{r['pass']:,}/{r['tested']:,} · {r.get('flaky', 0)} flaky</span></div>
          </div>
          <div class="track"><div class="fill" style="width:{r['rate']}%;background:{c}"></div></div>
        </div>""")
    s4 = f"""
    <h2>Agent scorecard · Week {esc(wk['key'])}</h2>
    <p class="sub">Summed across {wk.get('runs', 1)} nights (judgeable installs without an API key).</p>
    <div class="card-stack">{''.join(rank_rows)}</div>
    <p class="note">Note: Agents are tested on different add-on pools (only the formats each supports), so rates reflect pool readiness.</p>
    """

    # Slide 5: Top Categories
    top_cats = [(cat, cnt) for cat, cnt in cat_pass.most_common() if cat != "other"][:5]
    max_cat = top_cats[0][1] if top_cats else 1
    cat_cards = []
    for cat, cnt in top_cats:
        label = cat.title().replace("Mcp", "MCP").replace("Ai", "AI")
        w_pct = round(100 * cnt / max_cat, 1)
        cat_cards.append(f"""
        <div class="bar-row">
          <div class="bar-head">
            <div class="bar-name">{esc(label)}</div>
            <div class="bar-nums">{cnt} <span>add-ons passing</span></div>
          </div>
          <div class="track"><div class="fill" style="width:{w_pct}%"></div></div>
        </div>""")
    s5 = f"""
    <h2>Top passing categories</h2>
    <p class="sub">Categories with at least one passing install on {esc(d_lbl)} (ranked by add-on count).</p>
    <div class="card-stack">{''.join(cat_cards)}</div>
    <p class="note">Category leaderboards update automatically every night at skillmaxx.gilventures.ai/best/.</p>
    """

    # Slide 6: CTA
    s6 = f"""
    <div class="eyebrow"><span class="dot"></span>428+ ADD-ONS · FREE &amp; OPEN</div>
    <h1>Find add-ons tested in <em>your</em> agent.</h1>
    <p class="cover-sub" style="margin-bottom:36px">Filter by Claude Code, Codex, Grok Build, Cursor, or Pi and copy the exact verified install command.</p>
    <div class="cta-box">
      <div class="cta-label">Search the Directory</div>
      <div class="cta-url">skillmaxx.gilventures.ai</div>
      <div class="cta-desc">Per-agent compatibility matrix, 10-night history, and curated /best/ &amp; /works-in/ guides.</div>
    </div>
    <div class="cta-box" style="border-color:rgba(34,211,238,0.35)">
      <div class="cta-label" style="color:#22D3EE">Free Weekly Digest</div>
      <div class="cta-url">skillmaxx.gilventures.ai/newsletter/</div>
      <div class="cta-desc">Weekly leaderboard changes, confirmed breaks, and newly tested skills in your inbox.</div>
    </div>
    """

    slides = [s1, s2, s3, s4, s5, s6]
    return [
        wrap_slide(body, i + 1, total_slides, f"LEADERBOARD · {wk['key']}", "Swipe →" if i < total_slides - 1 else "skillmaxx.gilventures.ai")
        for i, body in enumerate(slides)
    ]


def render_slides_html(slides: list[str], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sync_playwright = None

    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if sync_playwright is not None:
        try:
            with sync_playwright() as p:
                try:
                    browser = p.chromium.launch()
                except Exception:
                    if not chrome:
                        raise
                    browser = p.chromium.launch(executable_path=chrome)
                page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
                for i, doc in enumerate(slides, 1):
                    page.set_content(doc, wait_until="load")
                    page.evaluate("document.fonts.ready")
                    out_png = out_dir / f"slide-{i:02d}.png"
                    page.screenshot(path=str(out_png))
                    paths.append(out_png)
                browser.close()
            return paths
        except Exception:
            paths.clear()

    if not chrome:
        raise RuntimeError("Neither Python playwright nor headless Chrome/Chromium is installed.")
    with tempfile.TemporaryDirectory(prefix="smx-carousel-") as td:
        for i, doc in enumerate(slides, 1):
            hp = Path(td) / f"slide-{i:02d}.html"
            hp.write_text(doc, encoding="utf-8")
            out_png = out_dir / f"slide-{i:02d}.png"
            subprocess.run(
                [
                    chrome,
                    "--headless",
                    "--disable-gpu",
                    "--no-sandbox",
                    "--hide-scrollbars",
                    "--window-size=1080,1350",
                    f"--screenshot={out_png}",
                    hp.as_uri(),
                ],
                check=True,
                capture_output=True,
            )
            paths.append(out_png)
    return paths


def zip_dir(folder: Path, zip_path: Path) -> Path:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(folder.glob("*.png")):
            zf.write(p, arcname=f"{folder.name}/{p.name}")
    return zip_path


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--format", choices=["news", "leaderboard", "all"], default="all")
    ap.add_argument("--date", help="Report date YYYY-MM-DD (default: latest in src/_data/reports.json)")
    ap.add_argument("--out", default="/workspace/carousels-samples")
    ap.add_argument("--zip", action="store_true")
    a = ap.parse_args(argv)

    data = load_data(a.date)
    d_str = data["rep"]["date"]
    out_root = Path(a.out)
    targets = ["news", "leaderboard"] if a.format == "all" else [a.format]

    for fmt in targets:
        slides = build_news_slides(data) if fmt == "news" else build_leaderboard_slides(data)
        name = f"{fmt}-{d_str}"
        dest = out_root / name
        pngs = render_slides_html(slides, dest)
        print(f"carousel {fmt}: rendered {len(pngs)} slides (1080x1350) -> {dest}")
        if a.zip:
            zp = zip_dir(dest, out_root / f"{name}.zip")
            print(f"carousel {fmt}: zipped -> {zp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
