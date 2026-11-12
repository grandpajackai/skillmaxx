#!/usr/bin/env python3
"""Grok install command pins. No sandbox and no network.

  python3 testing/test_grok_install.py
"""
import json, os, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
_argv = sys.argv
sys.argv = ["run_tests.py"]
import run_tests
sys.argv = _argv


class GrokInstallCommandTest(unittest.TestCase):
    def test_confirmed_qualifiers(self):
        native = ["https://github.com/xai-org/plugin-marketplace"]
        claude = ["https://github.com/anthropics/claude-plugins-official"]
        both = claude + native
        axiom = run_tests.grok_plugin_install("axiom", native)
        campaign = run_tests.grok_plugin_install("activecampaign", claude)
        base = run_tests.grok_plugin_install("base44", both)
        self.assertEqual(
            axiom,
            "grok plugin install axiom@xai-org/plugin-marketplace --trust 2>&1; echo ---LIST; grok plugin list 2>&1",
        )
        self.assertEqual(
            campaign,
            "grok plugin install activecampaign@claude-plugins-official --trust 2>&1; echo ---LIST; grok plugin list 2>&1",
        )
        self.assertEqual(
            base,
            "grok plugin install base44@xai-org/plugin-marketplace --trust 2>&1; echo ---LIST; grok plugin list 2>&1",
        )
        for cmd in (axiom, campaign, base):
            self.assertNotIn("@plugin-marketplace", cmd)
            self.assertNotIn("@local/", cmd)
        self.assertIsNone(run_tests.grok_plugin_install("other", ["https://github.com/openai/plugins"]))

    def test_catalog_examples_keep_the_same_case_set(self):
        with open(os.path.join(ROOT, "data/skills.json")) as f:
            items = json.load(f)["items"]
        by = {i["slug"]: i for i in items}
        self.assertIn("@xai-org/plugin-marketplace", run_tests.grok_plugin_install("axiom", by["axiom"]["listings"]))
        self.assertIn("@claude-plugins-official", run_tests.grok_plugin_install("activecampaign", by["activecampaign"]["listings"]))
        self.assertIn("@xai-org/plugin-marketplace", run_tests.grok_plugin_install("base44", by["base44"]["listings"]))
        listed = [
            i["slug"] for i in items
            if "plugin-marketplace" in " ".join(i.get("listings") or [])
            or "claude-plugins-official" in " ".join(i.get("listings") or [])
        ]
        built = [i["slug"] for i in items if run_tests.grok_plugin_install(i["slug"], i.get("listings"))]
        self.assertEqual(built, listed)
        run_tests.AG = ["grok_build", "claude_code"]
        run_tests.items = [by["axiom"], by["activecampaign"], by["base44"]]
        cmds = {(c[0]["slug"], c[1]): c[3] for c in run_tests.cases()}
        self.assertNotIn(("axiom", "claude_code"), cmds)
        self.assertIn("activecampaign@claude-plugins-official", cmds[("activecampaign", "claude_code")])
        self.assertIn("activecampaign@claude-plugins-official", cmds[("activecampaign", "grok_build")])
        self.assertIn("base44@xai-org/plugin-marketplace", cmds[("base44", "grok_build")])
        self.assertIn("activecampaign@claude-plugins-official --trust", cmds[("activecampaign", "grok_build")])

    def test_pass_check_still_reads_the_installed_line(self):
        ok = "Installed 1 plugin(s) from xAI Official: axiom\n---LIST\n  skills: axiom [git: https://github.com/axiomhq/skills.git] (xAI Official)\n"
        self.assertTrue(run_tests.grok_ok(ok))
        claude = "Installed 1 plugin(s) from claude-plugins-official: activecampaign\n---LIST\n  plug: activecampaign [git: https://example.com/p.git] (claude-plugins-official)\n"
        self.assertTrue(run_tests.grok_ok(claude))
        scan = "Couldn't scan every marketplace while resolving \"activecampaign\"\n---LIST\nNo plugins installed.\n"
        self.assertFalse(run_tests.grok_ok(scan))


if __name__ == "__main__":
    unittest.main()
