# Contact-form targets — 2026-10-29 (not submitted yet)

For a browser agent. Submit each form once, screenshot the confirmation, then update the company's row in growth/sponsors/PIPELINE.csv: status `Contacted`, date_contacted `2026-10-29`, outreach_sent `<Form> submitted <time> ET Oct 29 with OUTREACH.md pitch; confirmation shown`, next_follow_up `2026-11-05, then 2026-11-12 (final)`. Then send Brandon the one-line update (company, route, what was sent).

**Always use:** Name **Brandon Gil** · Company **SkillMaxx** · Email **skillmaxx@gilventures.ai** · Website **https://skillmaxx.gilventures.ai** · Role (if asked) Founder.

**Rules:** never give a phone number. If a form *requires* phone, a US state, a seat count or anything else we don't have or that would be untrue, **do not submit**: log it in PIPELINE notes as blocked with the reason and tell Brandon. Untick every marketing/newsletter opt-in. Don't book calls/demos. One submission per company.

Numbers in the messages are from the Oct 29 nightly (testing/results/2026-10-29.json). Each message is under 120 words.

| # | Company | Form URL | Slot offered |
|---|---|---|---|
| 1 | Resend | https://resend.com/contact | Newsletter ($19 for 1 issue / $59/mo for 4) |
| 2 | WorkOS | https://workos.com/contact | Newsletter ($19 for 1 issue / $59/mo for 4) |
| 3 | Clerk | https://clerk.com/contact/sales | Newsletter ($19 for 1 issue / $59/mo for 4) |
| 4 | Sanity | https://www.sanity.io/contact/sales | Newsletter ($19 for 1 issue / $59/mo for 4) |
| 5 | Langfuse | https://langfuse.com/talk-to-us | Newsletter ($19 for 1 issue / $59/mo for 4) |
| 6 | Netlify | https://www.netlify.com/contact/sales/ | Newsletter ($19 for 1 issue / $59/mo for 4) |

## 1. Resend

**Form URL:** https://resend.com/contact  
**Directory data:** yes: resend (plugin, development); 2026-10-29: pass on claude_code, grok_build  
**Fields seen:** email, message

**Enter:**
- Email: skillmaxx@gilventures.ai
- Message: (below)
- Only 2 fields. The page shows the form twice; use the one in the "Contact" section the URL scrolls to.

**Message:**

```
Hi! I'm Brandon. I run SkillMaxx, a free directory that install-tests agent plugins and MCP servers nightly across 5 coding agents, with public logs: https://skillmaxx.gilventures.ai/reports/latest/ Your Resend skills plugin installed clean in Claude Code and Grok Build last night. Honest ask: would you take a founding Newsletter slot ($19 for 1 issue, or $59/mo for 4)? Locked 6 months for the first 10 sponsors, always labeled Sponsored; money never changes a result. Brand new, tiny audience (that's why it's cheap); you'd get a monthly report with real numbers. A one-line "not now" helps too. Brandon, https://skillmaxx.gilventures.ai/advertise/
```

**Notes:** /contact redirects to /support#contact; form has only email + message (2 copies of the form on the page; use the one under "Contact"). This is the support form; no partnerships email published (founder addresses on /about are personal, not used).

## 2. WorkOS

**Form URL:** https://workos.com/contact  
**Directory data:** yes: workos (plugin, security); 2026-10-29: pass on claude_code, grok_build  
**Fields seen:** name, email, Question

**Enter:**
- Name: Brandon Gil
- Email: skillmaxx@gilventures.ai
- Question: (message below)

**Message:**

```
Hi! I'm Brandon. I run SkillMaxx, a free directory that install-tests agent plugins and MCP servers nightly across 5 coding agents, with public logs: https://skillmaxx.gilventures.ai/reports/latest/ Your WorkOS skills plugin (AuthKit, SSO, RBAC) installed clean in Claude Code and Grok Build last night. Honest ask: would you take a founding Newsletter slot ($19 for 1 issue, or $59/mo for 4)? Locked 6 months for the first 10 sponsors, always labeled Sponsored; money never changes a result. Brand new, tiny audience (that's why it's cheap); you'd get a monthly report with real numbers. A one-line "not now" helps too. Brandon, https://skillmaxx.gilventures.ai/advertise/
```

**Notes:** hello@workos.com is only in JSON-LD as customer support, so the contact form is the better route.

## 3. Clerk

**Form URL:** https://clerk.com/contact/sales  
**Directory data:** yes: clerk (plugin, development, Grok Build marketplace only); 2026-10-29: pass on grok_build  
**Fields seen:** email, country, name, website, job_function, job_level, message

**Enter:**
- Name: Brandon Gil
- Email: skillmaxx@gilventures.ai
- Website: https://skillmaxx.gilventures.ai
- Country: United States
- Job function: C-Suite
- Job level: C-level
- Message: (below)

**Message:**

```
Hi! I'm Brandon. I run SkillMaxx, a free directory that install-tests agent plugins and MCP servers nightly across 5 coding agents, with public logs: https://skillmaxx.gilventures.ai/reports/latest/ Your official Clerk plugin from the Grok Build marketplace installed clean in Grok Build last night. Honest ask: would you take a founding Newsletter slot ($19 for 1 issue, or $59/mo for 4)? Locked 6 months for the first 10 sponsors, always labeled Sponsored; money never changes a result. Brand new, tiny audience (that's why it's cheap); you'd get a monthly report with real numbers. A one-line "not now" helps too. Brandon, https://skillmaxx.gilventures.ai/advertise/
```

**Notes:** Sales form. Required dropdowns: Country (United States), Job function (C-Suite), Job level (C-level). No phone field.

## 4. Sanity

**Form URL:** https://www.sanity.io/contact/sales  
**Directory data:** yes: sanity (plugin, development); 2026-10-29: pass on claude_code, grok_build  
**Fields seen:** FirstName, LastName, Email, Company, companySize, notes

**Enter:**
- First name: Brandon · Last name: Gil
- Email: skillmaxx@gilventures.ai
- Company: SkillMaxx
- Company size: 1-99
- Notes / "How can we help": (message below)
- Marketing consent checkbox: leave UNTICKED
- Referral field (optional): leave blank

**Message:**

```
Hi! I'm Brandon. I run SkillMaxx, a free directory that install-tests agent plugins and MCP servers nightly across 5 coding agents, with public logs: https://skillmaxx.gilventures.ai/reports/latest/ Your Sanity plugin (MCP server, GROQ skills, slash commands) installed clean in Claude Code and Grok Build last night. Honest ask: would you take a founding Newsletter slot ($19 for 1 issue, or $59/mo for 4)? Locked 6 months for the first 10 sponsors, always labeled Sponsored; money never changes a result. Brand new, tiny audience (that's why it's cheap); you'd get a monthly report with real numbers. A one-line "not now" helps too. Brandon, https://skillmaxx.gilventures.ai/advertise/
```

**Notes:** Marketo sales form. Company size 1-99. Leave the marketing consent box unticked. No phone field seen.

## 5. Langfuse

**Form URL:** https://langfuse.com/talk-to-us  
**Directory data:** yes: langfuse + langfuse-observability (plugins, monitoring); 2026-10-29: both pass on claude_code, grok_build  
**Fields seen:** JS-rendered (Marketo) form; fields not visible to curl

**Enter:**
- Form is Marketo, rendered by JS (wait for "Loading form..." to finish).
- Likely fields: first/last name (Brandon / Gil), work email skillmaxx@gilventures.ai, company SkillMaxx, website https://skillmaxx.gilventures.ai, message (below).
- Any "use case"/"topic" dropdown: pick Partnership (or Other). Any team-size dropdown: smallest option.

**Message:**

```
Hi! I'm Brandon. I run SkillMaxx, a free directory that install-tests agent plugins and MCP servers nightly across 5 coding agents, with public logs: https://skillmaxx.gilventures.ai/reports/latest/ Both Langfuse plugins (Langfuse skills and Langfuse Observability) installed clean in Claude Code and Grok Build last night. Honest ask: would you take a founding Newsletter slot ($19 for 1 issue, or $59/mo for 4)? Locked 6 months for the first 10 sponsors, always labeled Sponsored; money never changes a result. Brand new, tiny audience (that's why it's cheap); you'd get a monthly report with real numbers. A one-line "not now" helps too. Brandon, https://skillmaxx.gilventures.ai/advertise/
```

**Notes:** Page names Akio Nuernberger, 'Enterprise & Partnerships'. Form loads by JS; if it requires a phone number, skip and log. No public partnerships email (press page lists a founder's personal address, not used).

## 6. Netlify

**Form URL:** https://www.netlify.com/contact/sales/  
**Directory data:** yes: netlify (Grok marketplace; pass grok_build, pi) + netlify-skills (pass claude_code, grok_build, pi); 2026-10-29  
**Fields seen:** HubSpot form (JS-rendered)

**Enter:**
- HubSpot form, rendered by JS.
- Likely fields: first/last name (Brandon / Gil), work email skillmaxx@gilventures.ai, company SkillMaxx, website https://skillmaxx.gilventures.ai, message (below).
- Any "what are you interested in" dropdown: pick Partnership/Other if offered, else General inquiry. Company size: smallest option.

**Message:**

```
Hi! I'm Brandon. I run SkillMaxx, a free directory that install-tests agent plugins and MCP servers nightly across 5 coding agents, with public logs: https://skillmaxx.gilventures.ai/reports/latest/ Your Netlify plugins installed clean last night: Netlify Skills in Claude Code, Grok Build and Pi, and the Grok marketplace Netlify plugin in Grok Build and Pi. Honest ask: would you take a founding Newsletter slot ($19 for 1 issue, or $59/mo for 4)? Locked 6 months for the first 10 sponsors, always labeled Sponsored; money never changes a result. Brand new, tiny audience (that's why it's cheap); you'd get a monthly report with real numbers. A one-line "not now" helps too. Brandon, https://skillmaxx.gilventures.ai/advertise/
```

**Notes:** If /contact/sales/ 404s, use https://www.netlify.com/contact/ and choose Sales. If the form requires phone, skip and log. Vercel was also offered Newsletter (still blocked).

## Not a form: X/LinkedIn-only lead (for Brandon)

**Expo** (https://expo.dev). Official Expo skills plugin passed in Claude Code, Codex and Grok Build in the Oct 29 nightly. There's no sales/partnership form (expo.dev/contact is a logged-in support form), no public general email, no phone. Handles from expo.dev: X **@expo** (https://twitter.com/expo), Bluesky **expo.dev**, LinkedIn https://www.linkedin.com/company/expo-dev.

Per OUTREACH.md #2, engage one of their posts first, then DM:

```
Hey Expo team, I run SkillMaxx (nightly install tests for agent skills/MCP across 5 coding agents). Your official Expo skills plugin installed clean in Claude Code, Codex and Grok Build last night (only 65 of 423 add-ons passed in 3+ agents).

Tiny ask when you have a sec: we're opening founding sponsor slots ($15–$29/mo, labeled, honest numbers). One-pager: skillmaxx.gilventures.ai/advertise/

If sponsorship isn't useful, what's one Expo setup we should be testing that we aren't?
```
