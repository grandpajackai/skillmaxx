#!/usr/bin/env python3
"""Dated blog draft queue + live-data token hydration (no LLM, offline, stdlib only).

Queued drafts live in growth/content/queue/YYYY-MM-DD--<target_stem>.njk, e.g.:
  growth/content/queue/2026-11-25--midweek-2026-48.njk  -> src/blog/midweek-2026-48.njk
  growth/content/queue/2026-11-29--week-2026-48.njk     -> src/blog/week-2026-48.njk

On or after the filename date, midweek_blog_auto.py and weekly_blog_auto.py load the
matching queued draft, refresh every [[SMX:...]] token from the latest committed nightly
files (reports.json, weeks.json, testing/results/<date>.json, data/skills.json, runNotes.json),
validate that no unfilled tokens or placeholders remain and that JSON-LD parses cleanly,
and write the rendered post into src/blog/.
"""
from __future__ import annotations

import glob
import html
import json
import os
import re
from datetime import date

AG = {"claude_code": "Claude Code", "codex": "Codex", "grok_build": "Grok Build", "cursor": "Cursor", "pi": "Pi"}
SLUG = {"claude_code": "claude-code", "codex": "codex", "grok_build": "grok-build", "cursor": "cursor", "pi": "pi"}
ORDER = ["claude_code", "grok_build", "codex", "cursor", "pi"]
TYPE_LABEL = {"plugin": "Plugins", "mcp-server": "MCP servers", "npm-mcp-package": "MCP servers (npm)", "skill": "Agent Skills"}
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
BEST_SLUGS = {"development", "productivity", "database", "mcp-servers", "monitoring", "security", "design", "deployment"}
TOKEN_RE = re.compile(r"\[\[SMX:([A-Z0-9_]+)\]\]")
BAD_RE = re.compile(r"<!--|TODO|TBD|FIXME|\bDRAFT\b|\bundefined\b|\bnan%", re.I)


def _fmt(s, year=False):
    x = date.fromisoformat(s) if isinstance(s, str) else s
    return f"{x.strftime('%b')} {x.day}" + (f", {x.year}" if year else "")


def _rate(p, t):
    return round(100 * p / t, 1) if t else 0.0


def _cat_label(raw):
    c = CAT_MERGE.get((raw or "other").lower(), (raw or "other").lower())
    lbl = re.sub(r"\b\w", lambda m: m.group(0).upper(), c)
    lbl = re.sub(r"\bMcp\b", "MCP", lbl)
    lbl = re.sub(r"\bAi\b", "AI", lbl)
    lbl = re.sub(r"\bApi\b", "API", lbl)
    slug = re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", c.replace("&", "and")))
    return c, lbl, slug


def find_queued(root: str, target_stem: str, run_date: str) -> tuple[str, str] | None:
    """Return (pub_date, path) for the queued draft matching target_stem when run_date >= pub_date."""
    qdir = os.path.join(root, "growth", "content", "queue")
    if not os.path.isdir(qdir):
        return None
    pat = re.compile(r"^(\d{4}-\d{2}-\d{2})-+(.+)\.njk$")
    for p in sorted(glob.glob(os.path.join(qdir, "*.njk"))):
        m = pat.match(os.path.basename(p))
        if not m:
            continue
        pub_date, stem = m.group(1), m.group(2)
        if stem == target_stem and run_date >= pub_date:
            return pub_date, p
    return None


def _group_res(res, skills_map):
    by_type_agent = {}
    by_type = {}
    by_cat = {}
    by_slug_agent = {}
    for x in res:
        slug = x["slug"]
        ag = x["agent"]
        ok = x["status"] == "pass"
        sk = skills_map.get(slug, {})
        t = sk.get("type", "unknown")
        by_type_agent.setdefault((t, ag), [0, 0])
        by_type_agent[(t, ag)][1] += 1
        by_type_agent[(t, ag)][0] += int(ok)

        tl = TYPE_LABEL.get(t, "Other")
        bt = by_type.setdefault(tl, {"n": 0, "p": 0, "addons": set()})
        bt["n"] += 1
        bt["p"] += int(ok)
        bt["addons"].add(slug)

        ck, cl, cs = _cat_label(sk.get("category"))
        if ck != "other":
            bc = by_cat.setdefault(ck, {"label": cl, "slug": cs, "n": 0, "p": 0, "addons": set(), "passing_addons": set()})
            bc["n"] += 1
            bc["p"] += int(ok)
            bc["addons"].add(slug)
            if ok:
                bc["passing_addons"].add(slug)

        by_slug_agent.setdefault(slug, {})[ag] = ok
    return by_type_agent, by_type, by_cat, by_slug_agent


def build_common_tokens(res, skills_items, rep, notes, lo_date, cd):
    skills_map = {i["slug"]: i for i in (skills_items or [])}
    by_type_agent, by_type, by_cat, by_slug_agent = _group_res(res or [], skills_map)

    # Type table
    if by_type:
        trows = "".join(
            f'<tr><th scope="row">{html.escape(t)}</th><td>{len(v["addons"])}</td><td>{v["n"]}</td><td>{v["p"]}</td><td>{_rate(v["p"], v["n"])}%</td></tr>'
            for t, v in sorted(by_type.items(), key=lambda kv: -kv[1]["n"])
        )
        type_table = (
            '<div class="tw"><table class="matrix"><thead><tr><th>Type</th><th>Add-ons</th><th>Installs</th><th>Passed</th><th>Rate</th></tr></thead>'
            f"<tbody>{trows}</tbody></table></div>"
        )
    else:
        type_table = "<p>No per-type install breakdown was recorded for this run.</p>"

    # Category table (top categories by tested installs)
    if by_cat:
        crows = []
        for ck, v in sorted(by_cat.items(), key=lambda kv: (-kv[1]["n"], kv[1]["label"])):
            if v["n"] < 5:
                continue
            name_cell = (
                f'<a href="/best/{html.escape(v["slug"])}/">{html.escape(v["label"])}</a>'
                if v["slug"] in BEST_SLUGS and len(v["passing_addons"]) >= 10
                else html.escape(v["label"])
            )
            crows.append(
                f'<tr><th scope="row">{name_cell}</th><td>{len(v["addons"])}</td><td>{v["n"]}</td><td>{v["p"]}</td><td>{_rate(v["p"], v["n"])}%</td></tr>'
            )
        category_table = (
            '<div class="tw"><table class="matrix"><thead><tr><th>Category</th><th>Add-ons</th><th>Installs</th><th>Passed</th><th>Rate</th></tr></thead>'
            f"<tbody>{''.join(crows[:10])}</tbody></table></div>"
        )
    else:
        category_table = "<p>No category breakdown was recorded for this run.</p>"

    # Status breakdown table from reports.json
    tot = rep.get("total") or 0
    ps = rep.get("pass") or 0
    nk = rep.get("needs_key") or 0
    brk = rep.get("broken") or 0
    pend = rep.get("pending") or 0
    flk = rep.get("flaky") or 0
    status_rows = [
        ("Passed (installed and loaded)", ps, _rate(ps, tot)),
        ("Needs your API key (keyless sandbox)", nk, _rate(nk, tot)),
        ("Broken (failed 2+ nights running)", brk, _rate(brk, tot)),
        ("Pending (1 failed night, re-checking)", pend, _rate(pend, tot)),
    ]
    status_table = (
        '<div class="tw"><table class="matrix"><thead><tr><th>Status</th><th>Installs</th><th>Share of total</th></tr></thead><tbody>'
        + "".join(f'<tr><th scope="row">{html.escape(lbl)}</th><td>{cnt:,}</td><td>{pct}%</td></tr>' for lbl, cnt, pct in status_rows)
        + "</tbody></table></div>"
        + f"<p class=\"muted\">Flaky installs across recent nights: {flk:,} (counted separately so one bad night doesn't mark a tool broken).</p>"
    )

    # MCP metrics across all 5 agents
    mcp_slugs = [s for s, sk in skills_map.items() if sk.get("type") in ("mcp-server", "npm-mcp-package") and s in by_slug_agent]
    mcp_all5 = [s for s in mcp_slugs if len(by_slug_agent[s]) == 5 and all(by_slug_agent[s].values())]
    mcp_all5.sort(key=lambda s: (-(skills_map[s].get("stars") or 0), (skills_map[s].get("name") or s).lower()))
    if mcp_all5:
        items_li = "".join(f'<li><a href="/skills/{html.escape(s)}/">{html.escape(skills_map[s].get("name") or s)}</a></li>' for s in mcp_all5[:12])
        more = f'<p class="muted">Plus {len(mcp_all5) - 12} more on the <a href="/best/mcp-servers/">MCP servers leaderboard</a>.</p>' if len(mcp_all5) > 12 else ""
        mcp_all5_list = f"<ul>{items_li}</ul>{more}"
    else:
        mcp_all5_list = '<p>See the <a href="/best/mcp-servers/">MCP servers leaderboard</a> for the latest cross-agent pass counts.</p>'

    npm_rates = []
    ref_rates = []
    mcp_agent_rows = []
    plugin_agent_rows = []
    for ag in ORDER:
        rp, rn = by_type_agent.get(("mcp-server", ag), [0, 0])
        np_, nn = by_type_agent.get(("npm-mcp-package", ag), [0, 0])
        if nn:
            npm_rates.append(_rate(np_, nn))
        if rn:
            ref_rates.append(f"{rp}/{rn}")
        mp, mn = rp + np_, rn + nn
        if mn:
            mcp_agent_rows.append(
                f'<tr><th scope="row"><a href="/works-in/{SLUG[ag]}/">{AG[ag]}</a></th>'
                f'<td>{rp}/{rn}</td><td>{np_}/{nn}</td><td>{mp}/{mn} ({_rate(mp, mn)}%)</td></tr>'
            )
        pp, pn = by_type_agent.get(("plugin", ag), [0, 0])
        if pn:
            plugin_agent_rows.append(
                f'<tr><th scope="row"><a href="/works-in/{SLUG[ag]}/">{AG[ag]}</a></th>'
                f'<td>{pp}</td><td>{pn}</td><td>{_rate(pp, pn)}%</td></tr>'
            )

    mcp_by_agent_table = (
        '<div class="tw"><table class="matrix"><thead><tr><th>Agent</th><th>Reference MCP</th><th>npm MCP</th><th>All MCP</th></tr></thead>'
        f"<tbody>{''.join(mcp_agent_rows)}</tbody></table></div>"
    ) if mcp_agent_rows else "<p>No per-agent MCP breakdown recorded for this run.</p>"

    plugin_by_agent_table = (
        '<div class="tw"><table class="matrix"><thead><tr><th>Agent</th><th>Passed</th><th>Tested plugins</th><th>Rate</th></tr></thead>'
        f"<tbody>{''.join(plugin_agent_rows)}</tbody></table></div>"
    ) if plugin_agent_rows else "<p>No per-agent plugin breakdown recorded for this run.</p>"

    # Grok vs Claude plugins
    plug_slugs = [s for s, sk in skills_map.items() if sk.get("type") == "plugin" and s in by_slug_agent]
    cc_only = [s for s in plug_slugs if by_slug_agent[s].get("claude_code") is True and by_slug_agent[s].get("grok_build") is False]
    gb_only = [s for s in plug_slugs if by_slug_agent[s].get("grok_build") is True and by_slug_agent[s].get("claude_code") is False]
    both_ok = [s for s in plug_slugs if by_slug_agent[s].get("claude_code") is True and by_slug_agent[s].get("grok_build") is True]
    cc_p, cc_n = by_type_agent.get(("plugin", "claude_code"), [0, 0])
    gb_p, gb_n = by_type_agent.get(("plugin", "grok_build"), [0, 0])
    grok_vs_claude = (
        '<div class="tw"><table class="matrix"><thead><tr><th>Comparison</th><th>Passed</th><th>Tested</th><th>Rate</th></tr></thead><tbody>'
        f'<tr><th scope="row"><a href="/works-in/claude-code/">Claude Code plugins</a></th><td>{cc_p}</td><td>{cc_n}</td><td>{_rate(cc_p, cc_n)}%</td></tr>'
        f'<tr><th scope="row"><a href="/works-in/grok-build/">Grok Build plugins</a></th><td>{gb_p}</td><td>{gb_n}</td><td>{_rate(gb_p, gb_n)}%</td></tr>'
        '</tbody></table></div>'
        f"<p>Across plugins tested in both agents on {_fmt(cd)}: {len(both_ok)} passed in both, {len(cc_only)} passed only in Claude Code, and {len(gb_only)} passed only in Grok Build (Grok Build also tests xAI marketplace plugins alongside Claude Code marketplace plugins).</p>"
    ) if (cc_n or gb_n) else "<p>No plugin comparison data was recorded for this run.</p>"

    # Pi MCP vs plugin
    pi_rows = []
    for tkey, label in (("mcp-server", "MCP servers (reference)"), ("npm-mcp-package", "MCP servers (npm)"), ("plugin", "Plugins (GitHub packages)"), ("skill", "Agent Skills")):
        p_, n_ = by_type_agent.get((tkey, "pi"), [0, 0])
        if n_:
            pi_rows.append(f'<tr><th scope="row">{label}</th><td>{p_}</td><td>{n_}</td><td>{_rate(p_, n_)}%</td></tr>')
    pi_mcp_p = by_type_agent.get(("mcp-server", "pi"), [0, 0])[0] + by_type_agent.get(("npm-mcp-package", "pi"), [0, 0])[0]
    pi_mcp_n = by_type_agent.get(("mcp-server", "pi"), [0, 0])[1] + by_type_agent.get(("npm-mcp-package", "pi"), [0, 0])[1]
    pi_plug_p, pi_plug_n = by_type_agent.get(("plugin", "pi"), [0, 0])
    pi_mcp_vs_plugin = (
        '<div class="tw"><table class="matrix"><thead><tr><th>Add-on type in Pi</th><th>Passed</th><th>Tested</th><th>Rate</th></tr></thead>'
        f"<tbody>{''.join(pi_rows)}</tbody></table></div>"
    ) if pi_rows else "<p>No Pi breakdown recorded for this run.</p>"

    # Caveats from runNotes.json
    caveats = [
        f'{_fmt(b["start"])}: new test baseline. {html.escape(b.get("why", "").rstrip("."))}.'
        for b in (notes or {}).get("baselines") or []
        if lo_date < b.get("start", "") <= cd
    ]
    caveats += [
        f'{_fmt(x["date"])}: no valid run.'
        for x in (notes or {}).get("no_valid_run") or []
        if lo_date < x.get("date", "") <= cd
    ]

    codex_mcp_p = by_type_agent.get(("mcp-server", "codex"), [0, 0])[0] + by_type_agent.get(("npm-mcp-package", "codex"), [0, 0])[0]
    codex_mcp_n = by_type_agent.get(("mcp-server", "codex"), [0, 0])[1] + by_type_agent.get(("npm-mcp-package", "codex"), [0, 0])[1]

    return {
        "TYPE_TABLE": type_table,
        "CATEGORY_TABLE": category_table,
        "STATUS_BREAKDOWN_TABLE": status_table,
        "MCP_ALL5_COUNT": str(len(mcp_all5)),
        "MCP_TOTAL_COUNT": str(len(mcp_slugs)),
        "MCP_NPM_PASS_RANGE": f"{min(npm_rates)}%–{max(npm_rates)}%" if npm_rates else "0%–0%",
        "MCP_ALL5_LIST": mcp_all5_list,
        "MCP_BY_AGENT_TABLE": mcp_by_agent_table,
        "PLUGIN_BY_AGENT_TABLE": plugin_by_agent_table,
        "GROK_VS_CLAUDE_PLUGINS_HTML": grok_vs_claude,
        "PI_MCP_VS_PLUGIN_HTML": pi_mcp_vs_plugin,
        "PI_PLUGIN_PASS": str(pi_plug_p),
        "PI_PLUGIN_TOTAL": str(pi_plug_n),
        "PI_PLUGIN_RATE": str(_rate(pi_plug_p, pi_plug_n)),
        "PI_MCP_PASS": str(pi_mcp_p),
        "PI_MCP_TOTAL": str(pi_mcp_n),
        "PI_MCP_RATE": str(_rate(pi_mcp_p, pi_mcp_n)),
        "CODEX_MCP_PASS": str(codex_mcp_p),
        "CODEX_MCP_TOTAL": str(codex_mcp_n),
        "CODEX_MCP_RATE": str(_rate(codex_mcp_p, codex_mcp_n)),
        "GROK_PLUGIN_PASS": str(gb_p),
        "GROK_PLUGIN_TOTAL": str(gb_n),
        "GROK_PLUGIN_RATE": str(_rate(gb_p, gb_n)),
        "CLAUDE_PLUGIN_PASS": str(cc_p),
        "CLAUDE_PLUGIN_TOTAL": str(cc_n),
        "CLAUDE_PLUGIN_RATE": str(_rate(cc_p, cc_n)),
        "CAVEAT_LIST": caveats,
    }


def render_queued_template(template_path: str, tokens: dict[str, str]) -> tuple[str | None, str]:
    """Substitute [[SMX:...]] tokens and validate the resulting .njk file. Returns (rendered_text, err)."""
    raw = open(template_path, encoding="utf-8").read()

    def repl(m):
        k = m.group(1)
        if k not in tokens:
            raise KeyError(k)
        return str(tokens[k])

    try:
        out = TOKEN_RE.sub(repl, raw)
    except KeyError as e:
        return None, f"unknown token [[SMX:{e.args[0]}]] in {os.path.basename(template_path)}"

    leftover = TOKEN_RE.findall(out)
    if leftover:
        return None, f"unfilled tokens {leftover} in {os.path.basename(template_path)}"

    m = re.match(r"---\n(.*?)\n---\n", out, re.S)
    if not m:
        return None, f"missing YAML front matter in {os.path.basename(template_path)}"
    head = m.group(1)
    body = out[m.end():]
    bad = sorted({x.group(0) for x in BAD_RE.finditer(body)})
    if bad:
        return None, f"placeholder text {bad} in {os.path.basename(template_path)}"
    jl_match = re.search(r"^jsonld:\s*(.+)$", head, re.M)
    if jl_match:
        try:
            json.loads(jl_match.group(1).strip())
        except ValueError as e:
            return None, f"invalid jsonld in {os.path.basename(template_path)}: {e}"
    return out, ""
