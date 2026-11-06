# Draft reply — Scott Lee / Qovia (DO NOT SEND yet)

**To:** scott@qovia.ai  
**From:** skillmaxx@gilventures.ai (or Brandon's preferred)  
**Subject:** Re: Qovia listing on SkillMaxx

---

Hi Scott,

Thanks for the clear submission — and for catching the form outage. FormSubmit (our free form backend) has been returning Cloudflare 522 for a few days, so the mailto fallback was the right call.

I verified the PyPI package, docs, and the remote MCP endpoint (`https://api.qovia.ai/mcp` answers initialize). Qovia is now in the SkillMaxx directory as an MCP server listing and will join the next nightly install pass across Claude Code, Codex, Grok Build, Cursor and Pi.

A heads-up on what "pass" means here: our sandboxes have no API keys, so we check that the agent can register/connect the server. Calls that need a Qovia key will show as needs-key, not broken. Once you have a preferred install line per agent (or a scoped trial key you want us to use for a tool-call check), send it and we'll rerun.

Listing: https://skillmaxx.gilventures.ai/skills/qovia/ (live after deploy)  
Submit form: https://skillmaxx.gilventures.ai/submit/

Thanks again for building this and for writing in.

Brandon  
SkillMaxx · https://skillmaxx.gilventures.ai

