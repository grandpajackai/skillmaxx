#!/usr/bin/env python3
"""Free, local 1080x1350 PNG & animated MP4 carousel generator for SkillMaxx.

Reads only real committed nightly data (src/_data/reports.json, weeks.json, latestRows.json,
data/skills.json, data/meta/meta.json) and renders HTML/CSS slides with bundled Inter & JetBrains Mono
fonts via headless Chromium (Python playwright, falling back to google-chrome/chromium CLI).
With --animate, records deterministic 30fps H.264 MP4 slides + still PNG fallbacks + preview.mp4 via ffmpeg.

Usage:
  python3 growth/carousels/generate.py [--format news|leaderboard|orgchart|maxxing|v2|all] [--date YYYY-MM-DD] [--out DIR] [--zip] [--animate] [--fps 30]
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



ANIM_JS = r"""
(function() {
  function clamp01(x) { return x < 0 ? 0 : (x > 1 ? 1 : x); }
  function easeOutCubic(x) { x = clamp01(x); return 1 - Math.pow(1 - x, 3); }
  function easeOutBack(x) {
    x = clamp01(x);
    const c1 = 1.70158, c3 = c1 + 1;
    return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2);
  }
  function easeInOutSine(x) { x = clamp01(x); return -(Math.cos(Math.PI * x) - 1) / 2; }

  const slide = document.querySelector('.slide');
  const duration = parseFloat(slide?.dataset?.duration || '5.5');

  const pops = Array.from(document.querySelectorAll('[data-anim="pop"]'));
  const rows = Array.from(document.querySelectorAll('[data-anim="row"]'));
  const counts = Array.from(document.querySelectorAll('[data-anim="count"]'));
  const badges = Array.from(document.querySelectorAll('[data-anim="badge-count"]'));
  const bars = Array.from(document.querySelectorAll('[data-anim="bar"]'));
  const floats = Array.from(document.querySelectorAll('[data-anim="float"]'));
  const trees = Array.from(document.querySelectorAll('[data-anim="org-tree"]'));
  const glows = Array.from(document.querySelectorAll('[data-anim="glow"]'));
  const sweeps = Array.from(document.querySelectorAll('[data-anim="step-sweep"]'));
  const dots = Array.from(document.querySelectorAll('.eyebrow .dot'));

  function formatNum(val, dec, comma) {
    let s = dec > 0 ? val.toFixed(dec) : String(Math.round(val));
    if (comma) {
      const parts = s.split('.');
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      s = parts.join('.');
    }
    return s;
  }

  function applyTime(t) {
    for (const el of pops) {
      const d = parseFloat(el.dataset.delay || '0');
      const dur = parseFloat(el.dataset.dur || '0.42');
      const fy = parseFloat(el.dataset.fromY || '20');
      const fs = parseFloat(el.dataset.fromScale || '0.90');
      const raw = clamp01((t - d) / dur);
      const p = raw <= 0 ? 0 : (el.dataset.ease === 'cubic' ? easeOutCubic(raw) : easeOutBack(raw));
      const op = easeOutCubic(clamp01(raw * 1.4));
      const y = fy * (1 - p);
      const s = fs + (1 - fs) * p;
      el.style.opacity = String(op);
      el.style.transform = `translate3d(0, ${y.toFixed(2)}px, 0) scale(${s.toFixed(4)})`;
    }

    for (const el of rows) {
      const d = parseFloat(el.dataset.delay || '0');
      const dur = parseFloat(el.dataset.dur || '0.40');
      const raw = clamp01((t - d) / dur);
      const p = easeOutCubic(raw);
      const op = easeOutCubic(clamp01(raw * 1.5));
      const y = -22 * (1 - p);
      const s = 0.97 + 0.03 * p;
      el.style.opacity = String(op);
      el.style.transform = `translate3d(0, ${y.toFixed(2)}px, 0) scale(${s.toFixed(4)})`;
    }

    for (const el of counts) {
      const d = parseFloat(el.dataset.delay || '0');
      const dur = parseFloat(el.dataset.dur || '0.65');
      const target = parseFloat(el.dataset.target || '0');
      const dec = parseInt(el.dataset.decimals || '0', 10);
      const comma = el.dataset.comma === '1';
      const prefix = el.dataset.prefix || '';
      const suffix = el.dataset.suffix || '';
      const raw = clamp01((t - d) / dur);
      const val = target * easeOutCubic(raw);
      el.textContent = prefix + formatNum(val, dec, comma) + suffix;
    }

    for (const el of badges) {
      const d = parseFloat(el.dataset.delay || '0');
      const dur = parseFloat(el.dataset.dur || '0.48');
      const passN = parseInt(el.dataset.pass || '5', 10);
      const totalN = parseInt(el.dataset.total || '5', 10);
      const suffix = el.dataset.suffix || ' PASS';
      const raw = clamp01((t - d) / dur);
      const cur = Math.round(passN * easeOutCubic(raw));
      el.textContent = `${cur}/${totalN}${suffix}`;
      if (raw > 0.85 && raw < 1.0) {
        const flash = Math.sin(((raw - 0.85) / 0.15) * Math.PI);
        el.style.transform = `scale(${(1 + 0.08 * flash).toFixed(3)})`;
      } else {
        el.style.transform = 'scale(1)';
      }
    }

    for (const el of bars) {
      const d = parseFloat(el.dataset.delay || '0');
      const dur = parseFloat(el.dataset.dur || '0.85');
      const w = parseFloat(el.dataset.width || '0');
      const raw = clamp01((t - d) / dur);
      const cur = w * easeOutCubic(raw);
      el.style.width = `${cur.toFixed(2)}%`;
    }

    for (const el of floats) {
      const per = parseFloat(el.dataset.period || '6.0');
      const phase = parseFloat(el.dataset.phase || '0');
      const baseRot = parseFloat(el.dataset.baseRot || '0');
      const ampY = parseFloat(el.dataset.ampY || '12');
      const ampX = parseFloat(el.dataset.ampX || '3');
      const ampRot = parseFloat(el.dataset.ampRot || '1.1');
      const theta = (2 * Math.PI * (t / per)) + phase;
      const dx = ampX * Math.cos(theta);
      const dy = ampY * Math.sin(theta);
      const rot = baseRot + ampRot * Math.sin(theta + 0.7);
      el.style.transform = `translate3d(${dx.toFixed(2)}px, ${dy.toFixed(2)}px, 0) rotate(${rot.toFixed(3)}deg)`;
    }

    for (const svg of trees) {
      const d = parseFloat(svg.dataset.delay || '0.65');
      const dur = parseFloat(svg.dataset.dur || '0.90');
      const raw = clamp01((t - d) / dur);
      const stem = svg.querySelector('#clip-stem');
      const bar = svg.querySelector('#clip-bar');
      const drops = svg.querySelector('#clip-drops');
      const dotsSvg = svg.querySelectorAll('circle[data-dot]');

      const pStem = easeOutCubic(clamp01(raw / 0.28));
      const pBar = easeOutCubic(clamp01((raw - 0.24) / 0.42));
      const pDrops = easeOutCubic(clamp01((raw - 0.60) / 0.40));

      if (stem) stem.setAttribute('height', (30 * pStem).toFixed(2));
      if (bar) {
        const half = 420 * pBar;
        bar.setAttribute('x', (468 - half).toFixed(2));
        bar.setAttribute('width', (half * 2).toFixed(2));
      }
      if (drops) drops.setAttribute('height', (48 * pDrops).toFixed(2));

      dotsSvg.forEach((c, idx) => {
        const dp = clamp01((raw - (0.68 + idx * 0.05)) / 0.18);
        const r = 4.5 * easeOutBack(dp);
        c.setAttribute('r', Math.max(0, r).toFixed(2));
        c.style.opacity = String(clamp01(dp * 2));
      });
    }

    for (const el of glows) {
      const d = parseFloat(el.dataset.delay || '0');
      const per = parseFloat(el.dataset.period || '3.0');
      const baseColor = el.dataset.glowColor || '198,244,50';
      const tt = Math.max(0, t - d);
      const pulse = t >= d ? 0.5 * (1 - Math.cos((2 * Math.PI * tt) / per)) : 0;
      const alpha = 0.10 + 0.16 * pulse;
      const spread = 36 + 24 * pulse;
      if (el.classList.contains('collage-hero')) {
        el.style.boxShadow = `0 24px 64px rgba(0,0,0,0.85), 0 0 ${spread.toFixed(1)}px rgba(${baseColor},${alpha.toFixed(3)})`;
      } else {
        el.style.boxShadow = `0 16px 46px rgba(0,0,0,0.55), 0 0 ${spread.toFixed(1)}px rgba(${baseColor},${alpha.toFixed(3)})`;
      }
    }

    if (sweeps.length) {
      sweeps.forEach((el, idx) => {
        const sStart = parseFloat(el.dataset.sweepStart || '1.75') + idx * 0.45;
        const sDur = 0.55;
        const raw = clamp01((t - sStart) / sDur);
        const pulse = raw > 0 && raw < 1 ? Math.sin(raw * Math.PI) : 0;
        if (pulse > 0.001) {
          el.style.boxShadow = `0 0 ${(32 * pulse).toFixed(1)}px rgba(198,244,50,${(0.28 * pulse).toFixed(3)})`;
        } else {
          el.style.boxShadow = '';
        }
      });
    }

    for (const dot of dots) {
      const pulse = 0.5 * (1 - Math.cos((2 * Math.PI * t) / duration * 2));
      dot.style.boxShadow = `0 0 ${(10 + 10 * pulse).toFixed(1)}px #C6F432`;
      dot.style.transform = `scale(${(1 + 0.18 * pulse).toFixed(3)})`;
    }
  }

  window.__setAnimTime = applyTime;
  applyTime(0);

  if (!window.__MANUAL_ANIM_CLOCK) {
    let t0 = null;
    function tick(now) {
      if (window.__MANUAL_ANIM_CLOCK) return;
      if (t0 === null) t0 = now;
      const elapsed = ((now - t0) / 1000) % duration;
      applyTime(elapsed);
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
})();
"""


def wrap_slide(
    body: str,
    idx: int,
    total: int,
    badge: str,
    footer_right: str = "Swipe →",
    animate: bool = False,
    duration: float = 5.5,
) -> str:
    dur_attr = f' data-duration="{duration:.2f}"' if animate else ""
    script_tag = f"<script>{ANIM_JS}</script>" if animate else ""
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><style>{font_css()}{BASE_CSS}</style></head>
<body>
  <div class="slide"{dur_attr}>
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
{script_tag}</body></html>"""


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




# ---------------------------------------------------------------------------
# v2 viral templates: orgchart (ai.byarsh style) + maxxing (artem collage style)
# ---------------------------------------------------------------------------

V2_CSS = """
.org-wrap {
  position: relative;
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.org-ceo {
  position: relative;
  display: flex;
  align-items: center;
  gap: 18px;
  background: #141418;
  border: 1.5px solid rgba(198,244,50,0.48);
  border-radius: 22px;
  padding: 20px 30px;
  box-shadow: 0 14px 40px rgba(0,0,0,0.45), 0 0 36px rgba(198,244,50,0.08);
}
.org-ceo-pill {
  position: absolute;
  top: -13px;
  left: 50%;
  transform: translateX(-50%);
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #0A0A0B;
  background: #C6F432;
  padding: 3px 12px;
  border-radius: 99px;
}
.org-tree-svg {
  width: 936px;
  height: 74px;
  display: block;
}
.org-grid {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
}
.org-dept {
  background: #121216;
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 20px;
  padding: 20px 12px 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 10px;
}
.org-dept-icon {
  width: 58px;
  height: 58px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  background: rgba(198,244,50,0.10);
  border: 1px solid rgba(198,244,50,0.28);
}
.org-dept-name {
  font-family: 'JetBrains Mono', monospace;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: #EDEDEF;
}
.org-dept-cnt {
  font-family: 'JetBrains Mono', monospace;
  font-size: 15px;
  color: #9CA3AF;
}
.dept-kicker {
  font-family: 'JetBrains Mono', monospace;
  font-size: 15px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #C6F432;
  margin-bottom: 10px;
}
.dept-tabs {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #121216;
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 99px;
  padding: 7px 10px;
  margin-bottom: 22px;
}
.dept-tab {
  flex: 1;
  text-align: center;
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 600;
  color: #71717A;
  padding: 7px 6px;
  border-radius: 99px;
  white-space: nowrap;
}
.dept-tab.active {
  background: rgba(198,244,50,0.16);
  border: 1px solid rgba(198,244,50,0.42);
  color: #C6F432;
}
.v2-rows {
  display: flex;
  flex-direction: column;
  gap: 11px;
}
.v2-row {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #121216;
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 18px;
  padding: 13px 18px;
}
.v2-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: #19191F;
  border: 1px solid rgba(255,255,255,0.12);
  display: grid;
  place-items: center;
  flex: none;
}
.v2-main {
  flex: 1;
  min-width: 0;
}
.v2-name-line {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 3px;
  white-space: nowrap;
  overflow: hidden;
}
.v2-name {
  font-size: 21px;
  font-weight: 700;
  color: #EDEDEF;
  overflow: hidden;
  text-overflow: ellipsis;
}
.v2-role {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 600;
  color: #C6F432;
  flex: none;
}
.v2-desc {
  font-size: 16px;
  color: #9CA3AF;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.v2-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: none;
}
.v2-idx {
  font-family: 'JetBrains Mono', monospace;
  font-size: 28px;
  font-weight: 700;
  color: #3F3F46;
  letter-spacing: -0.03em;
}
.v2-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  font-weight: 700;
  line-height: 1.15;
  text-align: center;
  padding: 6px 10px;
  border-radius: 10px;
  border: 1px solid rgba(198,244,50,0.36);
  background: rgba(198,244,50,0.09);
  color: #C6F432;
  min-width: 78px;
}
/* Collage slide for maxxing */
.collage-stage {
  position: relative;
  flex: 1;
  width: 100%;
}
.art-card {
  position: absolute;
  background: #141418;
  border: 1px solid rgba(255,255,255,0.16);
  border-radius: 18px;
  padding: 16px 18px;
  box-shadow: 0 18px 44px rgba(0,0,0,0.58);
}
.art-win-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(255,255,255,0.10);
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  color: #A1A1AA;
}
.art-dot { width: 9px; height: 9px; border-radius: 50%; }
.collage-hero {
  position: absolute;
  left: 50%;
  top: 49%;
  transform: translate(-50%, -50%);
  width: 780px;
  text-align: center;
  background: rgba(10,10,11,0.92);
  border: 1.5px solid rgba(198,244,50,0.38);
  border-radius: 28px;
  padding: 40px 38px;
  box-shadow: 0 24px 64px rgba(0,0,0,0.85), 0 0 60px rgba(198,244,50,0.12);
  z-index: 10;
}
.collage-hero h1 {
  font-size: 72px;
  margin-bottom: 16px;
}
.kw-box {
  background: linear-gradient(135deg, rgba(198,244,50,0.16), rgba(34,211,238,0.08));
  border: 2px solid rgba(198,244,50,0.58);
  border-radius: 24px;
  padding: 34px 36px;
  margin-top: 22px;
}
.kw-pill {
  display: inline-block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 32px;
  font-weight: 800;
  color: #0A0A0B;
  background: #C6F432;
  padding: 8px 22px;
  border-radius: 14px;
  margin: 0 6px;
}
.nl-cta-box {
  background: linear-gradient(135deg, rgba(198,244,50,0.16), rgba(34,211,238,0.08));
  border: 2px solid rgba(198,244,50,0.62);
  border-radius: 26px;
  padding: 32px 36px;
  margin-top: 22px;
  box-shadow: 0 16px 46px rgba(0,0,0,0.55), 0 0 40px rgba(198,244,50,0.12);
}
.nl-url-pill {
  display: inline-block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 24px;
  font-weight: 800;
  color: #0A0A0B;
  background: #C6F432;
  padding: 12px 24px;
  border-radius: 14px;
  margin: 12px 0 14px;
  letter-spacing: -0.01em;
}
"""


def _trim_desc(text: str, limit: int = 66) -> str:
    s = " ".join((text or "").split())
    if len(s) <= limit:
        return s
    cut = s[: limit - 1].rsplit(" ", 1)[0]
    return (cut or s[: limit - 1]).rstrip(",.;:-") + "…"


def _dept_svg(kind: str, color: str = "#C6F432", size: int = 26) -> str:
    icons = {
        "build": '<path d="M16 18l6-6-6-6M8 6l-6 6 6 6" stroke="C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
        "ops": '<path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" stroke="C" stroke-width="2.2" stroke-linecap="round" fill="none"/><circle cx="12" cy="12" r="3.5" stroke="C" stroke-width="2.2" fill="none"/>',
        "data": '<ellipse cx="12" cy="5.5" rx="7.5" ry="3" stroke="C" stroke-width="2.1" fill="none"/><path d="M4.5 5.5v13c0 1.66 3.36 3 7.5 3s7.5-1.34 7.5-3v-13M4.5 12c0 1.66 3.36 3 7.5 3s7.5-1.34 7.5-3" stroke="C" stroke-width="2.1" fill="none"/>',
        "work": '<rect x="3.5" y="3.5" width="7.5" height="7.5" rx="1.8" stroke="C" stroke-width="2.1" fill="none"/><rect x="13" y="3.5" width="7.5" height="7.5" rx="1.8" stroke="C" stroke-width="2.1" fill="none"/><rect x="3.5" y="13" width="7.5" height="7.5" rx="1.8" stroke="C" stroke-width="2.1" fill="none"/><rect x="13" y="13" width="7.5" height="7.5" rx="1.8" stroke="C" stroke-width="2.1" fill="none"/>',
        "guard": '<path d="M12 2.5l7.5 3.2v5.8c0 4.9-3.2 9.1-7.5 10.3-4.3-1.2-7.5-5.4-7.5-10.3V5.7L12 2.5z" stroke="C" stroke-width="2.1" fill="none"/><path d="M9 12.2l2.1 2.1 4.2-4.4" stroke="C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
    }
    inner = icons.get(kind, icons["build"]).replace("C", color)
    return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" style="display:block">{inner}</svg>'


def _collect_agent_status(data: dict) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = defaultdict(dict)
    for r in (data["latest_rows"].get("rows") or []):
        out[r["s"]][r["a"]] = r["st"]
    return out


def build_orgchart_slides(data: dict, animate: bool = False) -> list[str]:
    rep, skills = data["rep"], data["skills"]
    d_lbl = fmt_date(rep["date"])
    cc_stats = (rep.get("by") or {}).get("claude_code") or {}
    cc_pass = cc_stats.get("pass", 0)
    cc_broken = cc_stats.get("broken", 0)
    cc_judge = (cc_stats.get("total") or 0) - (cc_stats.get("needs_key") or 0)
    cc_pct = round(100 * cc_pass / cc_judge, 1) if cc_judge else 0
    ag_status = _collect_agent_status(data)

    depts = [
        {
            "key": "build",
            "tab": "BUILD",
            "title": "Build <em>&amp; Test</em>",
            "sub": "Code workflows, PR review, browsers, and developer tooling.",
            "color": "#C6F432",
            "cats": {"development", "testing", "developer tools", "migration"},
        },
        {
            "key": "ops",
            "tab": "OPS",
            "title": "Ship <em>&amp; Monitor</em>",
            "sub": "Deployments, error tracking, analytics, and cloud automation.",
            "color": "#22D3EE",
            "cats": {"monitoring", "deployment", "automation", "location"},
        },
        {
            "key": "data",
            "tab": "DATA",
            "title": "Data <em>&amp; Memory</em>",
            "sub": "Databases, vector stores, filesystem access, and context.",
            "color": "#A78BFA",
            "cats": {"database", "data & analytics", "files", "memory"},
        },
        {
            "key": "work",
            "tab": "WORK",
            "title": "Team <em>&amp; Work</em>",
            "sub": "Docs, issue trackers, design tools, and everyday workflows.",
            "color": "#F59E0B",
            "cats": {"productivity", "design", "learning", "reasoning", "utilities", "math", "communication", "creativity", "education & research", "other"},
        },
        {
            "key": "guard",
            "tab": "GUARD",
            "title": "Security <em>&amp; MCPs</em>",
            "sub": "Security scanners plus standalone npm MCP packages.",
            "color": "#22C55E",
            "cats": {"security", "mcp (npm)"},
        },
    ]

    # Partition ALL passing Claude Code skills into the 5 departments cleanly
    dept_items: dict[str, list[dict]] = {d["key"]: [] for d in depts}
    for slug, ag_map in ag_status.items():
        if ag_map.get("claude_code") != "pass":
            continue
        sk = skills.get(slug)
        if not sk:
            continue
        raw_cat = (sk.get("category") or "other").lower()
        target_key = "work"
        for d in depts:
            if raw_cat in d["cats"]:
                target_key = d["key"]
                break
        pass_cnt = sum(1 for v in ag_map.values() if v == "pass")
        total_cnt = len(ag_map)
        dept_items[target_key].append({
            "slug": slug,
            "name": sk.get("name") or slug,
            "type_lbl": TYPE_LABEL.get(sk.get("type", ""), "Add-on"),
            "desc": sk.get("description") or "",
            "pass_cnt": pass_cnt,
            "total_cnt": total_cnt,
            "stars": sk.get("stars") or 0,
        })

    def _clean_showcase(it: dict) -> bool:
        d = (it.get("desc") or "").strip()
        if "[deprecated]" in d.lower():
            return False
        return all(ord(ch) < 128 or ch in "—–…·•’‘“”×★✔✖→" for ch in d + it.get("name", ""))

    for k in dept_items:
        dept_items[k].sort(
            key=lambda x: (_clean_showcase(x), x["pass_cnt"] == x["total_cnt"], x["pass_cnt"], x["stars"], x["name"].lower()),
            reverse=True,
        )

    total_slides = 7

    # Slide 1: Hook + Org Chart
    dept_cards_html = []
    for d_idx, d in enumerate(depts):
        cnt = len(dept_items[d["key"]])
        c = d["color"]
        pop_attr = f' data-anim="pop" data-delay="{1.35 + d_idx * 0.12:.2f}" data-dur="0.40" data-from-y="20" data-from-scale="0.86"' if animate else ""
        cnt_attr = f' data-anim="count" data-delay="{1.40 + d_idx * 0.12:.2f}" data-dur="0.50" data-target="{cnt}" data-suffix=" verified"' if animate else ""
        dept_cards_html.append(f"""
        <div class="org-dept" style="border-color:rgba(255,255,255,0.14)"{pop_attr}>
          <div class="org-dept-icon" style="border-color:{c}55;background:{c}18">{_dept_svg(d["key"], c, 28)}</div>
          <div class="org-dept-name" style="color:{c}">{esc(d["tab"])}</div>
          <div class="org-dept-cnt"{cnt_attr}>{cnt} verified</div>
        </div>""")

    ceo_anim = ' data-anim="pop" data-delay="0.22" data-dur="0.44" data-from-y="16" data-from-scale="0.88"' if animate else ""
    if animate:
        tree_svg = """
      <svg class="org-tree-svg" viewBox="0 0 936 74" fill="none" data-anim="org-tree" data-delay="0.60" data-dur="0.90">
        <defs>
          <clipPath id="treeClip">
            <rect id="clip-stem" x="458" y="0" width="20" height="0"/>
            <rect id="clip-bar" x="468" y="20" width="0" height="16"/>
            <rect id="clip-drops" x="0" y="28" width="936" height="0"/>
          </clipPath>
        </defs>
        <g clip-path="url(#treeClip)">
          <path d="M468 0 V28 M84 28 H852 M84 28 V74 M276 28 V74 M468 28 V74 M660 28 V74 M852 28 V74"
                stroke="#C6F432" stroke-opacity="0.55" stroke-width="2.5" stroke-dasharray="6 6"/>
        </g>
        <circle data-dot="1" cx="84" cy="70" r="0" fill="#C6F432"/>
        <circle data-dot="1" cx="276" cy="70" r="0" fill="#22D3EE"/>
        <circle data-dot="1" cx="468" cy="70" r="0" fill="#A78BFA"/>
        <circle data-dot="1" cx="660" cy="70" r="0" fill="#F59E0B"/>
        <circle data-dot="1" cx="852" cy="70" r="0" fill="#22C55E"/>
      </svg>"""
    else:
        tree_svg = """
      <svg class="org-tree-svg" viewBox="0 0 936 74" fill="none">
        <path d="M468 0 V28 M84 28 H852 M84 28 V74 M276 28 V74 M468 28 V74 M660 28 V74 M852 28 V74"
              stroke="#C6F432" stroke-opacity="0.55" stroke-width="2.5" stroke-dasharray="6 6"/>
        <circle cx="84" cy="70" r="4.5" fill="#C6F432"/>
        <circle cx="276" cy="70" r="4.5" fill="#22D3EE"/>
        <circle cx="468" cy="70" r="4.5" fill="#A78BFA"/>
        <circle cx="660" cy="70" r="4.5" fill="#F59E0B"/>
        <circle cx="852" cy="70" r="4.5" fill="#22C55E"/>
      </svg>"""

    sc1_p = ' data-anim="pop" data-delay="2.05" data-dur="0.40" data-from-y="18" data-from-scale="0.92"' if animate else ""
    sc2_p = ' data-anim="pop" data-delay="2.18" data-dur="0.40" data-from-y="18" data-from-scale="0.92"' if animate else ""
    sc3_p = ' data-anim="pop" data-delay="2.31" data-dur="0.40" data-from-y="18" data-from-scale="0.92"' if animate else ""
    sc1_c = f' data-anim="count" data-delay="2.10" data-dur="0.65" data-target="{cc_pct}" data-decimals="1" data-suffix="%"' if animate else ""
    sc2_c = f' data-anim="count" data-delay="2.23" data-dur="0.65" data-target="{cc_pass}"' if animate else ""
    sc3_c = f' data-anim="count" data-delay="2.36" data-dur="0.60" data-target="{cc_broken}"' if animate else ""

    s1 = f"""
    <div class="eyebrow"><span class="dot"></span>NIGHTLY SANDBOX LOGS · {esc(d_lbl.upper())}</div>
    <h1><em>{cc_pass}</em> skills that actually install in Claude Code.</h1>
    <p class="cover-sub" style="margin-bottom:28px">Re-installed every night in fresh containers ({cc_pct}% clean pass rate). One core agent, five departments.</p>
    <div class="org-wrap">
      <div class="org-ceo"{ceo_anim}>
        <div class="org-ceo-pill">CORE AGENT</div>
        <div class="org-dept-icon" style="width:62px;height:62px">{_dept_svg("build", "#C6F432", 32)}</div>
        <div>
          <div style="font-size:30px;font-weight:800;letter-spacing:-0.02em">Claude Code</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:17px;color:#C6F432">{cc_pass} / {cc_judge} judgeable clean · 5 skipped (API key)</div>
        </div>
      </div>
      {tree_svg}
      <div class="org-grid">{''.join(dept_cards_html)}</div>
    </div>
    <div class="stat-grid" style="margin-top:28px;margin-bottom:0">
      <div class="stat-card" style="padding:22px 24px"{sc1_p}><div class="stat-val lime" style="font-size:44px"{sc1_c}>{cc_pct}%</div><div class="stat-lbl">Claude Code clean<br>install rate</div></div>
      <div class="stat-card" style="padding:22px 24px"{sc2_p}><div class="stat-val" style="font-size:44px"{sc2_c}>{cc_pass}</div><div class="stat-lbl">Verified add-ons<br>(sum of 5 depts)</div></div>
      <div class="stat-card" style="padding:22px 24px"{sc3_p}><div class="stat-val" style="font-size:44px"{sc3_c}>{cc_broken}</div><div class="stat-lbl">Broken installs<br>kept visible tonight</div></div>
    </div>
    <p class="note">Every count above sums strictly to tonight&apos;s {cc_pass} passing Claude Code installs. No sponsored ranks.</p>
    """

    # Slides 2-6: One slide per department (7 numbered rows each)
    dept_slides = []
    for idx, d in enumerate(depts, 1):
        items = dept_items[d["key"]]
        c = d["color"]
        tabs = []
        for d2 in depts:
            act = " active" if d2["key"] == d["key"] else ""
            style = f' style="background:{c}22;border-color:{c}66;color:{c}"' if act else ""
            dot = "• " if act else ""
            tabs.append(f'<div class="dept-tab{act}"{style}>{dot}{esc(d2["tab"])}</div>')

        rows_html = []
        for r_i, it in enumerate(items[:7], 1):
            star_str = f" · {fmt_stars(it['stars'])}" if it["stars"] else ""
            badge_txt = f"{it['pass_cnt']}/{it['total_cnt']} PASS"
            r_delay = 0.24 + (r_i - 1) * 0.21
            row_anim = f' data-anim="row" data-delay="{r_delay:.2f}" data-dur="0.40"' if animate else ""
            b_anim = (
                f' data-anim="badge-count" data-delay="{r_delay + 0.14:.2f}" data-dur="0.48"'
                f' data-pass="{it["pass_cnt"]}" data-total="{it["total_cnt"]}" data-suffix=" PASS"'
                if animate
                else ""
            )
            rows_html.append(f"""
            <div class="v2-row"{row_anim}>
              <div class="v2-icon" style="border-color:{c}44">{_dept_svg(d["key"], c, 22)}</div>
              <div class="v2-main">
                <div class="v2-name-line">
                  <div class="v2-name">{esc(it["name"])}</div>
                  <div class="v2-role" style="color:{c}">{esc(it["type_lbl"])}{esc(star_str)}</div>
                </div>
                <div class="v2-desc">{esc(_trim_desc(it["desc"], 66) or "Verified clean install in tonight's Claude Code sandbox.")}</div>
              </div>
              <div class="v2-right">
                <div class="v2-idx">{r_i:02d}</div>
                <div class="v2-badge" style="color:{c};border-color:{c}55;background:{c}14"{b_anim}>{badge_txt}</div>
              </div>
            </div>""")

        dept_slides.append(f"""
        <div class="dept-kicker" style="color:{c}">DEPARTMENT {idx} OF 5 · {esc(d["tab"])} · {len(items)} VERIFIED</div>
        <h2 style="margin-bottom:8px">{d["title"]}</h2>
        <p class="sub" style="font-size:21px;margin-bottom:18px">{esc(d["sub"])}</p>
        <div class="dept-tabs">{''.join(tabs)}</div>
        <div class="v2-rows">{''.join(rows_html)}</div>
        """)

    # Slide 7: Subscribe to the free newsletter CTA
    r1_a = ' data-anim="row" data-delay="0.25" data-dur="0.38"' if animate else ""
    r2_a = ' data-anim="row" data-delay="0.52" data-dur="0.38"' if animate else ""
    r3_a = ' data-anim="row" data-delay="0.79" data-dur="0.38"' if animate else ""
    cta_a = ' data-anim="pop" data-delay="1.15" data-dur="0.46" data-from-y="22" data-from-scale="0.93"' if animate else ""
    cta_g = ' data-anim="glow" data-delay="1.65" data-period="3.35"' if animate else ""

    s7 = f"""
    <div class="eyebrow"><span class="dot"></span>{cc_pass} VERIFIED · {cc_broken} BROKEN KEPT VISIBLE</div>
    <h1><em>{cc_pass}</em> clean installs. Delivered weekly.</h1>
    <p class="cover-sub" style="margin-bottom:26px">Every Sunday: the verified Claude Code stack, 5-agent compatibility shifts, and raw failure logs.</p>
    <div class="card-stack" style="gap:14px">
      <div class="item-row"{r1_a}>
        <div>
          <div class="item-title">01 · Filter by your coding agent</div>
          <div class="item-desc">Claude Code ({cc_pass} pass), Grok Build, Codex, Cursor, or Pi.</div>
        </div>
        <span class="pill lime">LIVE MATRIX</span>
      </div>
      <div class="item-row"{r2_a}>
        <div>
          <div class="item-title">02 · Copy the tested install command</div>
          <div class="item-desc">No guessing marketplace names or broken npm flags.</div>
        </div>
        <span class="pill cyan">COPY-PASTE</span>
      </div>
      <div class="item-row"{r3_a}>
        <div>
          <div class="item-title">03 · Spot confirmed breaks first</div>
          <div class="item-desc">Tonight&apos;s {cc_broken} broken Claude add-ons stay public with raw exit logs.</div>
        </div>
        <span class="pill amber">RAW LOGS</span>
      </div>
    </div>
    <div class="nl-cta-box"{cta_a}>
      <div class="cta-label">Subscribe to the free newsletter</div>
      <div style="font-size:34px;font-weight:800;line-height:1.25">
        Get the nightly results every week. <span style="color:#C6F432">Free.</span>
      </div>
      <div class="nl-url-pill"{cta_g}>https://skillmaxx.gilventures.ai/newsletter/</div>
      <div class="cta-desc" style="font-size:19px">All {cc_pass} live at <b style="color:#EDEDEF">skillmaxx.gilventures.ai/works-in/claude-code/</b></div>
    </div>
    """

    all_slides = [s1, *dept_slides, s7]
    durations = [6.0, 5.5, 5.5, 5.5, 5.5, 5.5, 5.0]
    return [
        wrap_slide(
            f"<style>{V2_CSS}</style>" + body,
            i + 1,
            total_slides,
            f"CLAUDE STACK · {fmt_short(rep['date']).upper()}",
            "Swipe →" if i < total_slides - 1 else "Free Sunday newsletter",
            animate=animate,
            duration=durations[i],
        )
        for i, body in enumerate(all_slides)
    ]


def build_maxxing_slides(data: dict, animate: bool = False) -> list[str]:
    rep, wk, skills = data["rep"], data["wk"], data["skills"]
    d_lbl = fmt_date(rep["date"])
    tested = rep.get("tested") or rep["total"]
    addons = rep.get("addons") or len(skills)
    rate = round(100 * rep["pass"] / tested, 1) if tested else 0
    ag_status = _collect_agent_status(data)

    by = rep.get("by") or {}
    cc = by.get("claude_code") or {}
    gb = by.get("grok_build") or {}
    cx = by.get("codex") or {}
    cu = by.get("cursor") or {}
    pi = by.get("pi") or {}

    five_of_five = []
    for slug, ag_map in ag_status.items():
        if len(ag_map) == 5 and all(v == "pass" for v in ag_map.values()):
            sk = skills.get(slug) or {}
            five_of_five.append({
                "slug": slug,
                "name": sk.get("name") or slug,
                "type_lbl": TYPE_LABEL.get(sk.get("type", ""), "MCP"),
                "desc": sk.get("description") or "",
                "stars": sk.get("stars") or 0,
            })
    five_of_five.sort(key=lambda x: (x["stars"], x["name"].lower()), reverse=True)

    total_slides = 6

    # Slide 1: Artifact Collage Hook (centered main card + levitating surrounding cards)
    def _fl(base_rot: float, phase: float, amp_y: float = 13.0, amp_x: float = 3.0, amp_rot: float = 1.1) -> str:
        if not animate:
            return ""
        return (
            f' data-anim="float" data-period="6.0" data-base-rot="{base_rot}"'
            f' data-phase="{phase:.2f}" data-amp-y="{amp_y:.1f}" data-amp-x="{amp_x:.1f}" data-amp-rot="{amp_rot:.1f}"'
        )

    hero_glow = ' data-anim="glow" data-delay="0" data-period="6.0"' if animate else ""

    s1 = f"""
    <div class="collage-stage">
      <!-- Top-left: Permission / Sandbox modal -->
      <div class="art-card" style="top:20px;left:2px;width:308px;transform:rotate(-4deg)"{_fl(-4.0, 0.00, 13.0, 3.0, 1.1)}>
        <div class="art-win-bar"><span class="art-dot" style="background:#EF4444"></span><span class="art-dot" style="background:#F59E0B"></span><span class="art-dot" style="background:#22C55E"></span>sandbox_check.sh</div>
        <div style="font-size:16px;font-weight:600;margin-bottom:10px">Install in fresh Docker?</div>
        <div style="display:flex;gap:8px;font-family:'JetBrains Mono',monospace;font-size:13px">
          <span style="padding:5px 12px;border-radius:8px;background:#C6F432;color:#0A0A0B;font-weight:700">Allow</span>
          <span style="padding:5px 12px;border-radius:8px;background:#1F1F26;color:#A1A1AA">No Keys</span>
        </div>
      </div>

      <!-- Top-center: Terminal install -->
      <div class="art-card" style="top:14px;left:328px;width:320px;transform:rotate(2deg);border-color:rgba(198,244,50,0.34)"{_fl(2.0, 1.05, 11.0, 2.5, 0.9)}>
        <div class="art-win-bar"><span class="art-dot" style="background:#C6F432"></span>claude — skillmaxx</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:14px;color:#C6F432;margin-bottom:6px">&gt; {rep['pass']:,} / {tested:,} clean</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:13px;color:#D4D4D8">✔ {rate}% judgeable pass</div>
      </div>

      <!-- Top-right: SKILL.md diskette / file card -->
      <div class="art-card" style="top:24px;right:2px;width:255px;transform:rotate(4deg)"{_fl(4.0, 2.10, 14.0, 3.0, 1.2)}>
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">
          <span style="font-family:'JetBrains Mono',monospace;font-size:16px;font-weight:700;color:#22D3EE">SKILL.md</span>
          <span class="pill cyan">{addons:,}</span>
        </div>
        <div style="font-size:14px;color:#9CA3AF">Plugins, skills &amp; MCP servers tested nightly</div>
      </div>

      <!-- Mid-left: 02:00 AM ET clock -->
      <div class="art-card" style="top:220px;left:-4px;width:270px;transform:rotate(-3deg);border-color:rgba(245,158,11,0.40)"{_fl(-3.0, 3.14, 12.0, 3.5, 1.0)}>
        <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#FCD34D;margin-bottom:4px">CRON · NIGHTLY RUN</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:38px;font-weight:800;color:#F59E0B;letter-spacing:-0.03em">02:00 AM</div>
        <div style="font-size:13px;color:#9CA3AF">America/New_York · {esc(d_lbl)}</div>
      </div>

      <!-- Mid-right: Raw fail warning -->
      <div class="art-card" style="top:224px;right:-4px;width:280px;transform:rotate(3deg);border-color:rgba(239,68,68,0.40)"{_fl(3.0, 4.19, 13.0, 3.5, 1.0)}>
        <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#FCA5A5;margin-bottom:4px">RAW FAILURE LOGS</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:15px;color:#EDEDEF">✖ {cc.get('broken', 0)} broken in Claude</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:13px;color:#9CA3AF;margin-top:4px">✖ {pi.get('broken', 0)} broken in Pi · stays public</div>
      </div>

      <!-- Center Focal Headline -->
      <div class="collage-hero"{hero_glow}>
        <div class="eyebrow" style="margin:0 auto 18px"><span class="dot"></span>{addons:,} ADD-ONS · 5 CODING AGENTS</div>
        <h1>The art of<br><em>SkillMaxxing</em>.</h1>
        <p style="font-size:25px;color:#A1A1AA;line-height:1.4">Stop installing agent skills that break on step one. Real sandbox logs from {esc(d_lbl)}.</p>
      </div>

      <!-- Bottom-left: 5/5 badge -->
      <div class="art-card" style="bottom:74px;left:4px;width:292px;transform:rotate(-2.5deg);border-color:rgba(34,197,94,0.42)"{_fl(-2.5, 5.24, 14.0, 3.0, 1.1)}>
        <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#86EFAC;margin-bottom:4px">CROSS-AGENT ELITE</div>
        <div style="font-size:26px;font-weight:800;color:#EDEDEF">{len(five_of_five)} pass in <span style="color:#22C55E">5 / 5</span></div>
        <div style="font-size:14px;color:#9CA3AF">Claude · Grok · Codex · Cursor · Pi</div>
      </div>

      <!-- Bottom-center: Query pill -->
      <div class="art-card" style="bottom:44px;left:322px;width:308px;transform:rotate(1.5deg)"{_fl(1.5, 2.62, 11.0, 2.5, 0.9)}>
        <div style="font-size:14px;color:#9CA3AF;margin-bottom:6px">Before you run <code style="color:#C6F432">npx</code> or <code style="color:#C6F432">/plugin</code>:</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:15px;font-weight:600;color:#EDEDEF">skillmaxx.gilventures.ai ↗</div>
      </div>

      <!-- Bottom-right: Agent breakdown -->
      <div class="art-card" style="bottom:70px;right:4px;width:280px;transform:rotate(-3deg)"{_fl(-3.0, 0.78, 13.0, 3.0, 1.1)}>
        <div style="font-family:'JetBrains Mono',monospace;font-size:13px;color:#A78BFA;margin-bottom:6px">5 SANDBOX AGENTS</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:14px;line-height:1.5;color:#D4D4D8">
          Claude {cc.get('pass', 0)} · Grok {gb.get('pass', 0)}<br>
          Codex {cx.get('pass', 0)} · Pi {pi.get('pass', 0)} · Cursor {cu.get('pass', 0)}
        </div>
      </div>
    </div>
    """

    # Slide 2: What Broke Tonight
    broke_map = defaultdict(list)
    name_of = {}
    for b in (rep.get("broke") or []) + (wk.get("broke") or []):
        sl = b.get("slug")
        if sl:
            name_of[sl] = b.get("name") or (skills.get(sl) or {}).get("name") or sl
            ag = AG_SHORT.get(b.get("agent"), "")
            if ag and ag not in broke_map[sl]:
                broke_map[sl].append(ag)
    if len(broke_map) < 4:
        for sl, ag_map in ag_status.items():
            fails = [AG_SHORT[a] for a, st in ag_map.items() if st in ("fail", "broken") and a in AG_SHORT]
            if fails and sl not in broke_map:
                name_of[sl] = (skills.get(sl) or {}).get("name") or sl
                broke_map[sl] = fails
            if len(broke_map) >= 6:
                break

    broke_rows = []
    for i, (sl, ags) in enumerate(list(broke_map.items())[:5], 1):
        r_anim = f' data-anim="row" data-delay="{0.65 + (i - 1) * 0.24:.2f}" data-dur="0.40"' if animate else ""
        broke_rows.append(f"""
        <div class="v2-row" style="border-color:rgba(239,68,68,0.28)"{r_anim}>
          <div class="v2-icon" style="border-color:rgba(239,68,68,0.40);background:rgba(239,68,68,0.10)">{_dept_svg("guard", "#FCA5A5", 22)}</div>
          <div class="v2-main">
            <div class="v2-name-line">
              <div class="v2-name">{esc(name_of.get(sl, sl))}</div>
              <div class="v2-role" style="color:#FCA5A5">FAILING</div>
            </div>
            <div class="v2-desc">Failed clean sandbox install in: {esc(', '.join(ags))}</div>
          </div>
          <div class="v2-right">
            <div class="v2-idx">{i:02d}</div>
            <div class="v2-badge" style="color:#FCA5A5;border-color:rgba(239,68,68,0.45);background:rgba(239,68,68,0.12)">BROKE</div>
          </div>
        </div>""")

    pill_specs = [
        ("Pi", pi.get("broken", 0)),
        ("Grok", gb.get("broken", 0)),
        ("Claude", cc.get("broken", 0)),
        ("Codex", cx.get("broken", 0)),
        ("Cursor", cu.get("broken", 0)),
    ]
    pills_html = []
    for p_i, (ag_lbl, br_n) in enumerate(pill_specs):
        p_anim = f' data-anim="pop" data-delay="{0.15 + p_i * 0.10:.2f}" data-dur="0.34" data-from-y="10" data-from-scale="0.88"' if animate else ""
        c_anim = f' data-anim="count" data-delay="{0.18 + p_i * 0.10:.2f}" data-dur="0.45" data-target="{br_n}" data-prefix="{ag_lbl}: " data-suffix=" broken"' if animate else ""
        pills_html.append(f'<span class="pill red"{p_anim}{c_anim}>{ag_lbl}: {br_n} broken</span>')

    s2 = f"""
    <div class="dept-kicker" style="color:#FCA5A5">01 · THE TRAP</div>
    <h2>Most lists hide what <em style="color:#FCA5A5">broke</em>.</h2>
    <p class="sub" style="margin-bottom:22px">Real broken installs from {esc(d_lbl)} — zero retries hidden, zero paid removals.</p>
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px">{''.join(pills_html)}</div>
    <div class="v2-rows">{''.join(broke_rows)}</div>
    <p class="note">An add-on is only marked confirmed &ldquo;broke&rdquo; after failing two consecutive nightly runs.</p>
    """

    # Slide 3: 5/5 Cross-Agent Elite
    elite_rows = []
    for i, it in enumerate(five_of_five[:7], 1):
        r_d = 0.30 + (i - 1) * 0.21
        r_anim = f' data-anim="row" data-delay="{r_d:.2f}" data-dur="0.40"' if animate else ""
        b_anim = f' data-anim="badge-count" data-delay="{r_d + 0.14:.2f}" data-dur="0.48" data-pass="5" data-total="5" data-suffix=" PASS"' if animate else ""
        elite_rows.append(f"""
        <div class="v2-row"{r_anim}>
          <div class="v2-icon" style="border-color:rgba(34,197,94,0.42)">{_dept_svg("guard", "#22C55E", 22)}</div>
          <div class="v2-main">
            <div class="v2-name-line">
              <div class="v2-name">{esc(it["name"])}</div>
              <div class="v2-role" style="color:#86EFAC">{esc(it["type_lbl"])}</div>
            </div>
            <div class="v2-desc">{esc(_trim_desc(it["desc"], 66) or "Passed clean install in all 5 coding agents.")}</div>
          </div>
          <div class="v2-right">
            <div class="v2-idx">{i:02d}</div>
            <div class="v2-badge" style="color:#86EFAC;border-color:rgba(34,197,94,0.42);background:rgba(34,197,94,0.12)"{b_anim}>5/5 PASS</div>
          </div>
        </div>""")

    elite_cnt_attr = f' data-anim="count" data-delay="0.05" data-dur="0.65" data-target="{len(five_of_five)}"' if animate else ""
    s3 = f"""
    <div class="dept-kicker" style="color:#86EFAC">02 · CROSS-AGENT ELITE</div>
    <h2><span{elite_cnt_attr}>{len(five_of_five)}</span> add-ons pass in <em style="color:#22C55E">all 5 agents</em>.</h2>
    <p class="sub" style="margin-bottom:20px">Installed cleanly across Claude Code, Grok Build, Codex, Cursor, and Pi on {esc(d_lbl)}.</p>
    <div class="v2-rows">{''.join(elite_rows)}</div>
    """

    # Slide 4: 5-Agent Reality Check
    by_rows = []
    for ag, v in by.items():
        judge = (v.get("total") or 0) - (v.get("needs_key") or 0)
        if judge > 0:
            by_rows.append((v.get("pass", 0) / judge, ag, v.get("pass", 0), judge, v.get("broken", 0)))
    by_rows.sort(reverse=True)
    bars = []
    for b_i, (r, ag, ps, j, br) in enumerate(by_rows):
        pct = round(r * 100, 1)
        c = AG_COLOR.get(ag, "#C6F432")
        d0 = 0.22 + b_i * 0.16
        row_a = f' data-anim="pop" data-delay="{d0:.2f}" data-dur="0.38" data-from-y="16" data-from-scale="0.96" data-ease="cubic"' if animate else ""
        bar_a = f' data-anim="bar" data-delay="{d0 + 0.18:.2f}" data-dur="0.85" data-width="{pct}"' if animate else ""
        pct_a = f' data-anim="count" data-delay="{d0 + 0.18:.2f}" data-dur="0.85" data-target="{pct}" data-decimals="1" data-suffix="%"' if animate else ""
        fill_style = f"width:0%;background:{c}" if animate else f"width:{pct}%;background:{c}"
        bars.append(f"""
        <div class="bar-row"{row_a}>
          <div class="bar-head">
            <div class="bar-name"><span style="width:14px;height:14px;border-radius:50%;background:{c};display:inline-block"></span>{esc(AG_NAME.get(ag, ag))}</div>
            <div class="bar-nums"><span style="color:#EDEDEF;font-size:24px;font-weight:600;margin-left:0"{pct_a}>{pct}%</span> <span>{ps}/{j} clean · {br} broken</span></div>
          </div>
          <div class="track"><div class="fill" style="{fill_style}"{bar_a}></div></div>
        </div>""")

    s4 = f"""
    <div class="dept-kicker">03 · 5-AGENT MATRIX</div>
    <h2>Where installs <em>pass</em> — and stall.</h2>
    <p class="sub" style="margin-bottom:24px">Judgeable clean installs on {esc(d_lbl)} ({rep.get('needs_key', 0)} runs skipped for API keys).</p>
    <div class="card-stack">{''.join(bars)}</div>
    <p class="note">Each agent runs in its own isolated container with zero pre-cached plugins.</p>
    """

    # Slide 5: 3-Step Clean Setup Loop
    st1_a = ' data-anim="pop" data-delay="0.25" data-dur="0.42" data-from-y="20" data-from-scale="0.94"' if animate else ""
    st2_a = ' data-anim="pop" data-delay="0.70" data-dur="0.42" data-from-y="20" data-from-scale="0.94"' if animate else ""
    st3_a = ' data-anim="pop" data-delay="1.15" data-dur="0.42" data-from-y="20" data-from-scale="0.94"' if animate else ""
    sw_a = ' data-anim="step-sweep" data-sweep-start="1.75"' if animate else ""

    s5 = f"""
    <div class="dept-kicker" style="color:#22D3EE">04 · THE WORKFLOW</div>
    <h2>The 3-step <em style="color:#22D3EE">SkillMaxxing</em> loop.</h2>
    <p class="sub" style="margin-bottom:28px">How to wire up a clean agent stack without debugging broken READMEs.</p>
    <div class="card-stack" style="gap:18px">
      <div class="card" style="padding:26px 28px;border-color:rgba(198,244,50,0.32)"{st1_a}{sw_a}>
        <div style="font-family:'JetBrains Mono',monospace;font-size:16px;color:#C6F432;margin-bottom:8px">STEP 01 · PICK YOUR AGENT</div>
        <div style="font-size:27px;font-weight:700;margin-bottom:8px">Start on <code style="color:#C6F432">/works-in/&lt;agent&gt;/</code></div>
        <div class="item-desc" style="font-size:20px">See only skills, plugins, and MCP servers that installed cleanly in last night&apos;s sandbox.</div>
      </div>
      <div class="card" style="padding:26px 28px;border-color:rgba(34,211,238,0.32)"{st2_a}{sw_a}>
        <div style="font-family:'JetBrains Mono',monospace;font-size:16px;color:#22D3EE;margin-bottom:8px">STEP 02 · COPY TESTED COMMAND</div>
        <div style="font-size:27px;font-weight:700;margin-bottom:8px">Run the exact verified command</div>
        <div class="item-desc" style="font-size:20px">Claude <code style="color:#EDEDEF">/plugin install</code>, <code style="color:#EDEDEF">npx</code> MCP config, or Codex skill path — straight from passing runs.</div>
      </div>
      <div class="card" style="padding:26px 28px;border-color:rgba(167,139,250,0.32)"{st3_a}{sw_a}>
        <div style="font-family:'JetBrains Mono',monospace;font-size:16px;color:#A78BFA;margin-bottom:8px">STEP 03 · CHECK 10-NIGHT HISTORY</div>
        <div style="font-size:27px;font-weight:700;margin-bottom:8px">Spot flaky vs. rock-solid tools</div>
        <div class="item-desc" style="font-size:20px">Read raw failure logs before spending 20 minutes wondering why a server won&apos;t boot.</div>
      </div>
    </div>
    """

    # Slide 6: Subscribe to the free newsletter CTA
    m1_p = ' data-anim="pop" data-delay="0.25" data-dur="0.40" data-from-y="18" data-from-scale="0.90"' if animate else ""
    m2_p = ' data-anim="pop" data-delay="0.40" data-dur="0.40" data-from-y="18" data-from-scale="0.90"' if animate else ""
    m3_p = ' data-anim="pop" data-delay="0.55" data-dur="0.40" data-from-y="18" data-from-scale="0.90"' if animate else ""
    m1_c = f' data-anim="count" data-delay="0.30" data-dur="0.65" data-target="{rate}" data-decimals="1" data-suffix="%"' if animate else ""
    m2_c = f' data-anim="count" data-delay="0.45" data-dur="0.65" data-target="{addons}" data-comma="1"' if animate else ""
    nl_p = ' data-anim="pop" data-delay="1.05" data-dur="0.46" data-from-y="22" data-from-scale="0.93"' if animate else ""
    nl_g = ' data-anim="glow" data-delay="1.55" data-period="3.45"' if animate else ""

    s6 = f"""
    <div class="eyebrow"><span class="dot"></span>OPEN SOURCE · ZERO PAYWALL · {esc(d_lbl.upper())}</div>
    <h1>Stop guessing. <em>Read the logs.</em></h1>
    <p class="cover-sub" style="margin-bottom:26px">The {len(five_of_five)} cross-agent winners, new sandbox breaks, and copy-paste commands — in one free Sunday issue.</p>
    <div class="stat-grid" style="margin-top:0;margin-bottom:20px">
      <div class="stat-card"{m1_p}><div class="stat-val lime"{m1_c}>{rate}%</div><div class="stat-lbl">Clean pass rate<br>({rep['pass']:,}/{tested:,})</div></div>
      <div class="stat-card"{m2_p}><div class="stat-val"{m2_c}>{addons:,}</div><div class="stat-lbl">Skills, plugins<br>&amp; MCPs tested</div></div>
      <div class="stat-card"{m3_p}><div class="stat-val">$0</div><div class="stat-lbl">Free directory<br>&amp; weekly digest</div></div>
    </div>
    <div class="nl-cta-box" style="margin-top:0"{nl_p}>
      <div class="cta-label">Subscribe to the free newsletter</div>
      <div style="font-size:34px;font-weight:800;line-height:1.25">
        Get the nightly results every week. <span style="color:#C6F432">Free.</span>
      </div>
      <div class="nl-url-pill"{nl_g}>https://skillmaxx.gilventures.ai/newsletter/</div>
      <div class="cta-desc">Daily report, per-agent matrix, and raw failure logs at <b style="color:#EDEDEF">skillmaxx.gilventures.ai</b></div>
    </div>
    """

    all_slides = [s1, s2, s3, s4, s5, s6]
    durations = [6.0, 5.5, 5.5, 5.5, 5.0, 5.0]
    return [
        wrap_slide(
            f"<style>{V2_CSS}</style>" + body,
            i + 1,
            total_slides,
            f"SKILLMAXXING · {fmt_short(rep['date']).upper()}",
            "Swipe →" if i < total_slides - 1 else "Free Sunday newsletter",
            animate=animate,
            duration=durations[i],
        )
        for i, body in enumerate(all_slides)
    ]


def _find_chrome() -> str | None:
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if chrome:
        return chrome
    mac_chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    if mac_chrome.exists():
        return str(mac_chrome)
    return None


def _launch_playwright_browser(playwright):
    chrome = _find_chrome()
    try:
        return playwright.chromium.launch()
    except Exception:
        if not chrome:
            raise
        return playwright.chromium.launch(executable_path=chrome)


def render_slides_html(slides: list[str], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sync_playwright = None

    chrome = _find_chrome()
    if sync_playwright is not None:
        try:
            with sync_playwright() as p:
                browser = _launch_playwright_browser(p)
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


def render_slides_animated(slides: list[str], out_dir: Path, fps: int = 30) -> tuple[list[Path], list[Path], Path, list[float]]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required for --animate mode.")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Python playwright is required for --animate mode.") from exc

    out_dir.mkdir(parents=True, exist_ok=True)
    mp4_paths: list[Path] = []
    png_paths: list[Path] = []
    durations: list[float] = []

    with sync_playwright() as p:
        browser = _launch_playwright_browser(p)
        page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for i, doc in enumerate(slides, 1):
            page.set_content(doc, wait_until="load")
            page.evaluate("document.fonts.ready")
            dur = float(page.evaluate("parseFloat(document.querySelector('.slide')?.dataset?.duration || '5.5')"))
            page.evaluate("window.__MANUAL_ANIM_CLOCK = true")
            n_frames = max(1, int(round(dur * fps)))

            out_mp4 = out_dir / f"slide-{i:02d}.mp4"
            out_png = out_dir / f"slide-{i:02d}.png"

            cmd = [
                ffmpeg,
                "-y",
                "-loglevel",
                "error",
                "-f",
                "image2pipe",
                "-vcodec",
                "png",
                "-framerate",
                str(fps),
                "-i",
                "-",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-r",
                str(fps),
                "-crf",
                "18",
                "-preset",
                "medium",
                "-movflags",
                "+faststart",
                "-video_track_timescale",
                "15360",
                str(out_mp4),
            ]
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            last_png = b""
            for f_idx in range(n_frames):
                t_sec = f_idx / float(fps)
                page.evaluate(f"window.__setAnimTime && window.__setAnimTime({t_sec:.6f})")
                png_bytes = page.screenshot(type="png")
                proc.stdin.write(png_bytes)
                last_png = png_bytes
            proc.stdin.close()
            rc = proc.wait()
            if rc != 0:
                raise RuntimeError(f"ffmpeg failed on {out_mp4} (exit {rc})")

            # Write final-frame still PNG fallback
            out_png.write_bytes(last_png)
            mp4_paths.append(out_mp4)
            png_paths.append(out_png)
            durations.append(dur)
        browser.close()

    # Stitch full deck preview MP4
    preview_mp4 = out_dir / "preview.mp4"
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as tf:
        concat_path = Path(tf.name)
        for mp in mp4_paths:
            tf.write(f"file '{mp.resolve()}'\n")
    try:
        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-loglevel",
                "error",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_path),
                "-c",
                "copy",
                "-movflags",
                "+faststart",
                str(preview_mp4),
            ],
            check=True,
            capture_output=True,
        )
    finally:
        concat_path.unlink(missing_ok=True)

    return mp4_paths, png_paths, preview_mp4, durations


def zip_dir(folder: Path, zip_path: Path) -> Path:
    files = sorted([*folder.glob("*.png"), *folder.glob("*.mp4")])
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in files:
            zf.write(p, arcname=f"{folder.name}/{p.name}")
    return zip_path


BUILDERS = {
    "news": (build_news_slides, "news"),
    "leaderboard": (build_leaderboard_slides, "leaderboard"),
    "orgchart": (build_orgchart_slides, "v2-orgchart"),
    "maxxing": (build_maxxing_slides, "v2-maxxing"),
}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--format", choices=["news", "leaderboard", "orgchart", "maxxing", "v2", "all"], default="all")
    ap.add_argument("--date", help="Report date YYYY-MM-DD (default: latest in src/_data/reports.json)")
    ap.add_argument("--out", default="/workspace/carousels-samples")
    ap.add_argument("--zip", action="store_true")
    ap.add_argument("--animate", action="store_true", help="Render animated MP4 slides (1080x1350 H.264 30fps) + PNG fallbacks + preview.mp4")
    ap.add_argument("--fps", type=int, default=30, help="Frame rate for --animate (default: 30)")
    a = ap.parse_args(argv)

    data = load_data(a.date)
    d_str = data["rep"]["date"]
    out_root = Path(a.out)
    if a.format == "all":
        targets = ["news", "leaderboard", "orgchart", "maxxing"]
    elif a.format == "v2":
        targets = ["orgchart", "maxxing"]
    else:
        targets = [a.format]

    for fmt in targets:
        fn, prefix = BUILDERS[fmt]
        if a.animate:
            anim_prefix = f"v2-animated-{prefix[3:]}" if prefix.startswith("v2-") else f"animated-{prefix}"
            name = f"{anim_prefix}-{d_str}"
            dest = out_root / name
            try:
                slides = fn(data, animate=True)
            except TypeError:
                slides = fn(data)
            mp4s, pngs, preview, durs = render_slides_animated(slides, dest, fps=a.fps)
            tot_dur = sum(durs)
            print(
                f"carousel {fmt} (animated): {len(mp4s)} mp4s + {len(pngs)} pngs + {preview.name} "
                f"({tot_dur:.1f}s total @ {a.fps}fps) -> {dest}"
            )
        else:
            slides = fn(data)
            name = f"{prefix}-{d_str}"
            dest = out_root / name
            pngs = render_slides_html(slides, dest)
            print(f"carousel {fmt}: rendered {len(pngs)} slides (1080x1350) -> {dest}")
        if a.zip:
            zp = zip_dir(dest, out_root / f"{name}.zip")
            print(f"carousel {fmt}: zipped -> {zp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
