#!/usr/bin/env python3
"""Offline checks for standalone-skill cases (type "skill") in run_tests.py. No sandbox, no network.
Canned outputs are trimmed copies of real Mac sandbox output from 2026-11-16 (angular-testing)."""
import importlib.util, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0]]
spec = importlib.util.spec_from_file_location("rt", os.path.join(HERE, "run_tests.py")); rt = importlib.util.module_from_spec(spec); spec.loader.exec_module(rt)
IT = {"slug": "angular-testing", "type": "skill", "skill": {"source": "marmicode/skills", "name": "angular-testing"}}
OK = {
  "claude_code": '"skills":["angular-testing","deep-research","design"]',
  "codex": "angular-testing: Writes, fixes and reviews Angular tests\n/home/sbx/.agents/skills/angular-testing/SKILL.md",
  "grok_build": "  Skills (1)\n  \u2514 angular-testing  user",
  "cursor": "cursor-agent reads ~/.agents/skills\n/home/sbx/.agents/skills/angular-testing/SKILL.md:name: angular-testing",
  "pi": '"name":"skill:angular-testing"',
}
BAD = {
  "claude_code": '"skills":["deep-research","design"]',
  "codex": "",
  "grok_build": "  Skills (None)",
  "cursor": "cursor-agent reads ~/.agents/skills\ngrep: /home/sbx/.agents/skills/angular-testing/SKILL.md: No such file or directory",
  "pi": "",
}
fails = 0
for ag in rt.SKILL_AGENT:
  c = rt.skill_case(IT, ag)
  assert c and c[1] == ag and c[2] == "", ag
  cmd, check = c[3], c[4]
  assert f"npx -y {rt.SKILLS_CLI} add marmicode/skills --skill angular-testing -g -a {rt.SKILL_AGENT[ag]} -y" in cmd, cmd
  assert "DISABLE_TELEMETRY=1" in cmd and "---LIST" in cmd
  for name, out, want in (("ok", OK[ag], True), ("bad", BAD[ag], False)):
    got = check("install log\n---LIST\n" + out)
    if got != want: fails += 1; print(f"FAIL {ag} {name}: got {got}")
  # a different skill name must not pass on angular-testing's output
  other = rt.skill_case({**IT, "skill": {"source": "marmicode/skills", "name": "angular"}}, ag)
  if other[4]("x\n---LIST\n" + OK[ag]): fails += 1; print(f"FAIL {ag}: prefix name matched")
assert rt.skill_case({"slug": "x", "type": "skill"}, "codex") is None
print("ok" if not fails else f"{fails} failures"); sys.exit(1 if fails else 0)
