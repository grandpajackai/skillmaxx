#!/usr/bin/env python3
"""Build-time QA for _site (run after Eleventy). Fails (exit 1) when a built page shows template junk:
  - leaked Nunjucks/Liquid syntax in visible HTML: {# #}, {% %}, {{ }} (text inside <script>, <style>,
    <code>, <pre>, tag attributes and HTML comments is ignored, so JSON-LD and code samples don't trip it)
  - a newsletter card (section.nlcard) whose heading or subtext is empty or literally "true"/"false"
    (the Nov 2026 bug: .md pages rendered includes with Liquid, so `nlh or "..."` became `true`)
  - a newsletter card without the Beehiiv form placeholder (div.bhf[data-bhform])
Usage: python3 review/check_built_site.py [_site]"""
import re, sys, glob, os
root = sys.argv[1] if len(sys.argv) > 1 else "_site"
STRIP = re.compile(r"<(script|style|code|pre)\b.*?</\1>|<!--.*?-->", re.S | re.I)
LEAK = re.compile(r"\{#|#\}|\{%|%\}|\{\{|\}\}")
CARD = re.compile(r'<section class="[^"]*\bnlcard\b[^"]*"[^>]*>(.*?)</section>', re.S)
bad = []
files = glob.glob(os.path.join(root, "**", "*.html"), recursive=True)
for f in files:
    s = open(f, encoding="utf-8", errors="replace").read()
    vis = re.sub(r"<[^>]*>", " ", STRIP.sub("", s))  # visible text only (attribute JSON is not shown)
    for m in LEAK.finditer(vis):
        bad.append(f"{f}: leaked template syntax near: {vis[max(0, m.start() - 40):m.end() + 40]!r}")
        break
    for c in CARD.findall(s):
        h = re.search(r"<h2[^>]*>(.*?)</h2>", c, re.S); p = re.search(r"<p[^>]*>(.*?)</p>", c, re.S)
        for label, m in (("heading", h), ("subtext", p)):
            t = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""
            if label == "heading" and not t or t.lower() in ("true", "false", "undefined", "null"):
                bad.append(f"{f}: newsletter card {label} is {t!r}")
        if 'data-bhform="' not in c:
            bad.append(f"{f}: newsletter card has no Beehiiv form (div.bhf[data-bhform])")
print(f"checked {len(files)} pages: {len(bad)} problem(s)")
for b in bad[:50]: print("  " + b)
sys.exit(1 if bad else 0)
