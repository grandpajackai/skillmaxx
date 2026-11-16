#!/usr/bin/env python3
"""Turn growth/newsletter/issue-00N-beehiiv.md into paste-ready HTML for the Beehiiv editor.
Usage: python3 growth/newsletter/to_html.py growth/newsletter/issue-003-beehiiv.md  -> writes issue-003-beehiiv.html
The **Title/Subtitle/Preview text** lines become a header comment (type those into Beehiiv's fields);
everything after them becomes the email body. Needs the python `markdown` package."""
import re, sys, html, markdown
src = sys.argv[1]; s = open(src).read()
s = re.sub(r"^<!--.*?-->\n", "", s, flags=re.S)
meta = {}
for k in ("Title", "Subtitle", "Preview text"):
    m = re.search(rf"^\*\*{k}:\*\* (.+)$", s, flags=re.M)
    if m: meta[k] = m.group(1).strip(); s = s.replace(m.group(0) + "\n", "", 1)
body = markdown.markdown(s.strip(), extensions=["tables"])
body = re.sub(r'(?<![">])(https://skillmaxx\.gilventures\.ai/[^\s<"]*[^\s<".,)])', r'<a href="\1">\1</a>', body)
head = "<!--\n  Paste into Beehiiv: title, subtitle and preview text go in the post settings fields;\n  the HTML below goes in the editor (Insert > HTML snippet, or paste as rich text from a browser).\n" + \
       "".join(f"  {k}: {html.escape(v)}\n" for k, v in meta.items()) + "-->\n"
out = src.rsplit(".", 1)[0] + ".html"
open(out, "w").write(head + body + "\n")
print(out)
