PS="P.S. If you'd like the weekly install results yourself, the SkillMaxx newsletter is free: https://skillmaxx.gilventures.ai/newsletter/"
NEW=[ # company, to, subject, name, why-fit sentence, slot line
("InstantDB","hello@instantdb.com","InstantDB and the apps agents build","InstantDB team","Agent-built apps are a big share of what our readers ship, and a realtime backend is a natural pick for them."),
("Blacksmith","hello@blacksmith.sh","a $19 test in front of people running agent CI","Blacksmith team","Our readers run coding agents that open lots of PRs, so CI speed is a daily pain for them."),
("SerpApi","contact@serpapi.com","search tools for agents, from the install-test side","SerpApi team","Search is the first tool most agents get, and we see which search add-ons install cleanly every night."),
("Typesense","contact@typesense.org","open-source search in front of agent builders","Typesense team","Open-source search keeps coming up in the RAG and agent stacks our readers build."),
("Cerebras","info@cerebras.ai","fast inference, in front of people picking coding agents","Cerebras team","Speed is the first thing people notice when they pick a coding agent, so fast inference fits our readers."),
("Dify","business@dify.ai","a $19 test in front of people building agent workflows","Dify team","Your partner page says you work with ecosystem partners, and our readers build exactly these workflows."),
("Flowise","hello@flowiseai.com","a $19 test in front of people building agents","Flowise team","Visual agent builders and coding-agent users overlap a lot in our readership."),
("Fern","sales@buildwithfern.com","docs and SDKs, in front of people picking agent tools","Fern team","Good docs decide whether an agent can install and use a tool, which is exactly what we test."),
("Diffbot","sales@diffbot.com","web data for agents, from the install-test side","Diffbot team","Web data is one of the most-installed agent add-on types we test."),
("Oxylabs","hello@oxylabs.io","scraping and AI tools, in front of agent builders","Oxylabs team","Scraping and proxy tools with MCP support are a big share of what our readers install."),
("Scrapfly","sales@scrapfly.io","your MCP server and our nightly install tests","Scrapfly team","You ship an MCP server, and MCP installs are the core of what we test."),
("Zenrows","partnerships@zenrows.com","a $19 test in front of people wiring up scraping","Zenrows team","Your public partners page suggests you are open to this kind of placement, and scraping is a popular agent add-on category."),
("Patronus AI","contact@patronus.ai","evals for the people choosing agent tools","Patronus team","We test whether agent add-ons install; you test whether agents behave. Same reader, different step."),
("Strapi","marketing@strapi.io","a $19 test in front of people building with agents","Strapi team","Headless CMS is a common backend for the agent-built sites our readers ship."),
("Lightning AI","sales@lightning.ai","an AI dev platform in front of agent builders","Lightning team","Our readers are AI developers choosing their toolchain, which fits your platform."),
("Voyage AI","contact@voyageai.com","embeddings and rerankers, in front of agent builders","Voyage team","Retrieval quality is a constant topic among the agent builders who read us."),
("Cognee","info@cognee.ai","agent memory, from the install-test side","Cognee team","Memory is a category on our site that is still thin, so a memory tool would stand out."),
("Bruno","sales@usebruno.com","an API client in front of agent builders","Bruno team","Developers who work with coding agents still live in API clients all day."),
("Apidog","sales@apidog.com","your MCP server and our nightly install tests","Apidog team","You ship an MCP server, and MCP installs are the core of what we test."),
("Namespace","sales@namespace.so","fast CI in front of people running coding agents","Namespace team","Coding agents multiply PRs and CI runs, so CI speed matters more to our readers every month."),
]
def new_body(name,why):
    return f"""Hi {name},

I'm Brandon. I run SkillMaxx, a free directory that install-tests 430 agent skills, plugins and MCP servers nightly in Claude Code, Codex, Grok Build, Cursor and Pi (public logs: https://skillmaxx.gilventures.ai/reports/latest/). Last night 905 of 1,085 installs passed.

{why}

Honest ask: would you take a founding Newsletter slot at $19/issue ($59/mo for 4)? Locked 6 months for the first 10 sponsors. Always labeled Sponsored; money never changes a test result.

We launched in Oct 2026, so the audience is small (hence the price). You'd get a monthly report with real numbers, even small ones.

A one-line "not now" helps too.

Brandon
SkillMaxx · https://skillmaxx.gilventures.ai/advertise/

{PS}
"""
FU1=f"""Hi again, one nudge, then I'll leave you alone.

Since my last note we published this week's install scorecard: https://skillmaxx.gilventures.ai/reports/week/2026-47/

If sponsoring isn't a fit, a one-line "not now" is genuinely helpful, and so is "test this instead".

Brandon

{PS}
"""
FU2=f"""Last note from me on this.

Founding slots (first 10, 6-month rate lock) are still open; Featured stays month-to-month. Menu: https://skillmaxx.gilventures.ai/advertise/

If timing is wrong, I'll check back after we cross a real audience milestone rather than pinging again.

Thanks either way,
Brandon

{PS}
"""
FU=[("Chroma","hello@trychroma.com"),("Letta","contact@letta.com"),("Agno","hello@agno.com"),("Kilo Code","sales@kilo.ai"),("Socket","sales@socket.dev"),("Infisical","team@infisical.com"),("Scalekit","hi@scalekit.com"),("Knock","hello@knock.app"),("Speakeasy","sales@speakeasy.com"),("Brave Search API","api-sales@brave.com")]
