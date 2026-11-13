#!/usr/bin/env python3
"""Make the public archive page src/newsletter/issue-N.md from growth/newsletter/issue-00N-beehiiv.md.
Usage: python3 growth/newsletter/to_site.py N YYYY-MM-DD "one-line description" ["archive note"]"""
import re, sys, json
n, date, desc = sys.argv[1], sys.argv[2], sys.argv[3]; note = sys.argv[4] if len(sys.argv) > 4 else ""
s = open(f"growth/newsletter/issue-{int(n):03d}-beehiiv.md").read()
s = re.sub(r"^<!--.*?-->\n", "", s, flags=re.S)
title = re.search(r"^\*\*Title:\*\* (.+)$", s, flags=re.M).group(1).strip()
sub = re.search(r"^\*\*Subtitle:\*\* (.+)$", s, flags=re.M).group(1).strip()
s = re.sub(r"^\*\*(Title|Subtitle|Preview text):\*\* .+\n", "", s, flags=re.M).strip()
s = s.replace("https://raw.githubusercontent.com/grandpajackai/skillmaxx/master/growth/brand/beehiiv/skillmaxx-banner-1200x300.png", "/assets/newsletter/skillmaxx-banner-1200x300.png")
s = re.sub(r"\]\(https://skillmaxx\.gilventures\.ai/", "](/", s)
s = re.sub(r"(?<![(\[`])https://skillmaxx\.gilventures\.ai(/[^\s)`]*[^\s).,`])", r"[skillmaxx.gilventures.ai\1](\1)", s)  # bare URLs -> links
ld = {"@context": "https://schema.org", "@type": "Article", "headline": title, "datePublished": date, "author": {"@type": "Organization", "name": "SkillMaxx"},
      "publisher": {"@type": "Organization", "name": "SkillMaxx"}, "image": "https://skillmaxx.gilventures.ai/assets/newsletter/skillmaxx-banner-1200x300.png"}
fm = ["---", "layout: base.njk", f"title: {json.dumps(title)}", f"desc: {json.dumps(desc)}", f"permalink: /newsletter/issue-{n}/", "ogType: article",
      f"issue: {n}", f'issueDate: "{date}"', f"date: {date}", "tags: issues", "jsonld: " + json.dumps(ld, ensure_ascii=False), "---"]
out = "\n".join(fm) + f'\n<div class="wrap prose nlissue">\n<p class="crumbs"><a href="/">SkillMaxx</a> / <a href="/newsletter/">Newsletter</a> / Issue #{n}</p>\n' + \
      f'<h1 class="ph">{title}</h1>\n<p class="lead">{sub}</p>\n\n' + (f'<p class="callout">{note}</p>\n\n' if note else "") + s + '\n\n</div>\n{% include "nlembed.njk" %}\n'
open(f"src/newsletter/issue-{n}.md", "w").write(out)
print(f"src/newsletter/issue-{n}.md")
