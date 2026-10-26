# X reply playbook

## Watch (searches to save as columns / lists)
- `"claude code" (plugin OR skill OR mcp) -is:retweet`
- `"codex" (plugin OR "codex plugin" OR mcp) -is:retweet`
- `"grok build" OR "grok plugin"`
- `cursor ("mcp.json" OR "mcp server") (not working OR error OR help)`
- `(mcp server) ("doesn't work" OR "won't connect" OR "failed to connect")`
- `"which mcp" OR "best mcp" OR "favorite mcp" OR "recommend a skill"`
- `"SKILL.md" OR "agent skills"`
- Hashtags (low weight, mostly to find people): #ClaudeCode #MCP #AIagents #Codex #CursorAI #GrokBuild
- Accounts: see `FOLLOW.md`. Reply to *their followers' questions* more than to them.

## Rules
1. **Add value first.** Every reply must stand alone: a command, a gotcha, a number. If you delete the link, it should still be worth reading.
2. **Link only when it answers the question** (a specific skill page beats the homepage). At most 1 in 3 replies carries a link.
3. **Max 10–15 replies a day.** Spread them out. No more than 2 in the same thread.
4. **Never spam:** no copy-paste replies, no replying to unrelated viral posts, no @-mention blasts, no DMs unless someone asks.
5. **Be honest.** Only quote numbers from `testing/results/`. If we haven't tested it, say "haven't tested that one yet, adding it tonight".
6. **Tone:** cheeky, helpful, never smug about an agent or author. Failures are the ecosystem's, not a person's.
7. **Don't argue.** One correction max, with a log. Then leave.
8. **Sponsors / revenue:** never pitch in replies. If a tool company engages warmly twice, flag them for the outreach list (`growth/outreach/`).

## 10 reply templates (adapt every time, never paste verbatim)
1. **Install help:** "In {agent} it's `{command}`. The @marketplace bit matters, without it you can hit the 'which one?' error."
2. **Won't connect:** "Seen this. {server} installed fine for us but failed to connect in {agent} this week. Worth checking {tip}. Our log: {link}"
3. **"Does X work in Y?":** "We ran it Oct {d}: ✓ {agentA}, ✓ {agentB}, ✗ {agentC} ({reason}). Details: {link}"
4. **Grok ambiguity:** "Not you! Since this week {plugin} exists in 2+ marketplaces, so grok asks which. `grok plugin install {plugin}@{marketplace}` fixes it."
5. **Recommendation ask:** "For {use case}, {skill} passed in {n} agents for us, and {skill2} is the lighter option. Both have copy-paste installs here: {link}"
6. **Author shipped something:** "Congrats! Want us to run it through Claude Code, Codex, Grok, Cursor & Pi tonight? Happy to send the logs, good or bad."
7. **Grok auto-load tip:** "Fun fact: Grok Build auto-loads your Claude Code plugins, so you might already have this in Grok."
8. **Cursor MCP:** "Cursor tip: check `cursor-agent mcp list` shows `ready`. Anything else and the tools won't appear."
9. **Hot-take engagement:** "Agree, and the data backs it: {stat}. The hard part isn't writing skills, it's shipping them so they install everywhere."
10. **Untested item:** "Haven't tested that one yet. Adding it to tonight's run and I'll reply here with what happens."
