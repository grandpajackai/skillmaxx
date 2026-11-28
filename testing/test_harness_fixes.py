#!/usr/bin/env python3
"""Offline unit tests for nightly harness fixes in testing/run_tests.py. No sandbox, no network."""
import json, os, sys, types, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
_argv = sys.argv
sys.argv = ["run_tests.py"]
import run_tests as rt
sys.argv = _argv


class HarnessFixesTest(unittest.TestCase):
    def test_mcp_name_never_starts_with_digit(self):
        self.assertEqual(rt.mcp_name({"slug": "4sh-ui-kit"}), "s4shuikit")
        self.assertEqual(rt.mcp_name({"slug": "123"}), "s123")
        self.assertEqual(rt.mcp_name({"slug": "---"}), "srv")
        with open(os.path.join(ROOT, "data/skills.json")) as f:
            items = json.load(f)["items"]
        for it in items:
            if it["type"] in ("mcp-server", "npm-mcp-package"):
                n = rt.mcp_name(it)
                self.assertRegex(n, r"^[a-z][a-z0-9]{0,19}$", f"{it['slug']} -> {n!r}")

    def test_uvx_cmd_parsing(self):
        self.assertEqual(rt.uvx_cmd("uvx mcp-server-fetch"), "uvx mcp-server-fetch")
        self.assertEqual(rt.uvx_cmd("uvx --from claimidx[server] claimidx-mcp"), "uvx --from 'claimidx[server]' claimidx-mcp")
        self.assertIsNone(rt.uvx_cmd("npx -y @4sh/ui-kit"))
        self.assertIsNone(rt.uvx_cmd(None))
        self.assertIsNone(rt.uvx_cmd(""))

    def test_claude_plugin_enables_after_install(self):
        with open(os.path.join(ROOT, "data/skills.json")) as f:
            items = {i["slug"]: i for i in json.load(f)["items"]}
        rt.AG = ["claude_code"]
        rt.items = [items["monday-crm"]]
        rt.a = types.SimpleNamespace(limit=0)
        cs = rt.cases()
        self.assertEqual(len(cs), 1)
        cmd, check = cs[0][3], cs[0][4]
        self.assertIn("claude plugin install monday-crm@claude-plugins-official 2>&1 && (claude plugin enable monday-crm@claude-plugins-official", cmd)
        self.assertTrue(check("ok\n---LIST\n  ❯ monday-crm@claude-plugins-official\n    Status: ✔ enabled"))
        self.assertFalse(check("ok\n---LIST\n  ❯ monday-crm@claude-plugins-official\n    Status: ✘ disabled"))
        self.assertFalse(check("not found\n---LIST\nNo plugins installed."))

    def test_timeout_default_raised_from_150(self):
        with open(os.path.join(HERE, "run_tests.py")) as f:
            src = f.read()
        self.assertIn('"--timeout",type=int,default=300', src)

    def test_grok_doctor_error_line_kept_in_log(self):
        with open(os.path.join(HERE, "run_tests.py")) as f:
            src = f.read()
        self.assertIn('"timed out"', src)
        self.assertIn('"✗"', src)

    def test_sbx_keeps_npx_private(self):
        with open(os.path.join(HERE, "sbx.sh")) as f:
            sbx = f.read()
        self.assertNotIn("/tmp/skillmaxx-npm-cache/_npx", sbx)
        self.assertIn("ln -sfn /tmp/skillmaxx-npm-cache/_cacache /home/sbx/.npm/_cacache", sbx)


    def test_mcp_http_parses_remote_listings_and_skips_stdio(self):
        with open(os.path.join(ROOT, "data/skills.json")) as f:
            items = {i["slug"]: i for i in json.load(f)["items"]}
        xv = rt.mcp_http(items["xainvault"])
        self.assertEqual(xv["url"], "https://xainvault.com/mcp")
        self.assertEqual(xv["header"], "X-API-Key: $XAINVAULT_ACCESS_KEY")
        self.assertEqual(xv["transport"], "http")
        self.assertEqual(xv["name"], "xainvault")
        gv = rt.mcp_http(items["govisit"])
        self.assertEqual(gv["url"], "https://govisit.ai/mcp")
        self.assertIsNone(gv["header"])
        self.assertEqual(gv["name"], "govisit")
        qv = rt.mcp_http(items["qovia"])
        self.assertEqual(qv["url"], "https://api.qovia.ai/mcp")
        self.assertEqual(qv["header"], "Authorization: Bearer $QOVIA_API_KEY")
        self.assertIsNone(rt.mcp_http(items["claimidx"]))
        self.assertIsNone(rt.mcp_cmd(items["xainvault"]))
        self.assertIsNone(rt.mcp_cmd(items["govisit"]))
        self.assertIsNone(rt.mcp_cmd(items["qovia"]))
        self.assertIsNotNone(rt.mcp_cmd(items["claimidx"]))

    def test_remote_http_mcp_cases_for_documented_clients_only(self):
        with open(os.path.join(ROOT, "data/skills.json")) as f:
            items = {i["slug"]: i for i in json.load(f)["items"]}
        rt.AG = ["claude_code", "grok_build", "codex", "cursor", "pi"]
        rt.a = types.SimpleNamespace(limit=0)
        for slug in ("xainvault", "govisit", "qovia"):
            rt.items = [items[slug]]
            cs = rt.cases()
            agents = [c[1] for c in cs]
            self.assertEqual(agents, ["claude_code", "codex", "cursor"], slug)
            cmds = {c[1]: c[3] for c in cs}
            self.assertIn("--transport http", cmds["claude_code"])
            self.assertIn("--url", cmds["codex"])
            self.assertNotIn("mcp_probe.py", cmds["codex"])
            self.assertIn('"url"', cmds["cursor"])
            if slug == "xainvault":
                self.assertIn("X-API-Key", cmds["claude_code"])
                self.assertIn("https://xainvault.com/mcp", cmds["claude_code"])
                self.assertTrue(cs[0][4]("ok\n---LIST\nxainvault: Connected"))
                self.assertFalse(cs[0][4]("ok\n---LIST\nxainvault: Failed"))
            if slug == "govisit":
                self.assertIn("https://govisit.ai/mcp", cmds["claude_code"])
                self.assertNotIn("--header", cmds["claude_code"])
            if slug == "qovia":
                self.assertIn("Authorization: Bearer", cmds["claude_code"])
        # stdio MCP servers still get all 5 agents
        rt.items = [items["claimidx"]]
        cs = rt.cases()
        self.assertEqual([c[1] for c in cs], ["claude_code", "grok_build", "codex", "cursor", "pi"])


if __name__ == "__main__":
    unittest.main()
