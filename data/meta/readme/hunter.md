# Hunter for Claude

Hunter MCP connects Claude to your Hunter account through the Model Context Protocol (MCP). Ask in plain language, and Claude can find companies and people, find and verify email addresses, and enrich contacts. It can also organize leads and lists, run email sequences, and push leads to your CRM.

This plugin adds the Hunter MCP server and 13 Hunter skills to Claude Code and Claude Cowork.

- **Endpoint:** `https://mcp.hunter.io/mcp`
- **Transport:** Streamable HTTP
- **Authentication:** OAuth
- **Plans:** every Hunter plan, including Free. The credits and limits of your plan apply.

## Install

Install the plugin from the Claude plugin directory. Or run these commands in your shell:

```sh
claude plugin marketplace add hunter-io/claude-plugin
claude plugin install hunter@hunter
```

If your Claude Code build has no `claude plugin` command, use the slash commands in a session: `/plugin marketplace add hunter-io/claude-plugin`, then `/plugin install hunter@hunter`.

The Hunter tools load after you restart Claude Code or run `/reload-plugins`.

In Claude Cowork, you can also upload the plugin by hand: **Settings > Plugins > Upload custom plugin**.

Claude on the web and the Claude desktop chat do not need the plugin. In Claude, open **Customize > Connectors**, click **Add custom connector**, and enter `https://mcp.hunter.io/mcp`. The full steps for each client are at [hunter.io/mcp](https://hunter.io/mcp).

## Authentication

The plugin uses OAuth. No API key goes in a configuration file.

1. Ask Claude for a Hunter task. On the first tool call, Claude opens a Hunter sign-in page in your browser.
2. Sign in to Hunter and authorize access.

Claude never sees your Hunter password or your API key.

If you do not have a Hunter account, [sign up for free](https://hunter.io/users/sign_up).

## Skills

Hunter provides 13 skills. Claude starts a skill when your request matches it. You can also start a skill by name, for example `/hunter:email-finder`.

| Skill | What it does | Try saying... |
|-------|-------------|---------------|
| **Email Finder** | Find someone's email from their name and company | "Find Jane Smith's email at Stripe" |
| **Email Verifier** | Check if an email is deliverable | "Is jane@stripe.com valid?" |
| **Domain Search** | List all contacts at a company | "Who works at notion.com?" |
| **Company Enrichment** | Get company details from a domain | "Tell me about acme.com" |
| **Person Enrichment** | Get person details from an email | "What do you know about jane@stripe.com?" |
| **Discover** | Find companies by criteria and size their contacts (free) | "Fintech startups in France, 50-200 employees" |
| **Prospecting** | Full end-to-end pipeline | "Build a prospect list of CTOs at fintech startups" |
| **Build Sequences** | Create and run email outreach sequences | "Set up a 3-step sequence for my leads and start it" |
| **Manage Leads** | Create, tag, and organize leads | "Tag these contacts 'priority'" |
| **Lead Lists** | Build and organize leads lists | "Save these to a Q2 Outreach list" |
| **Company Lists** | Save and organize target accounts | "Save these companies to Target Accounts" |
| **Push to CRM** | Sync leads to your connected CRM | "Push my Q2 leads to HubSpot" |
| **Check Usage** | See your plan and remaining credits | "How many credits do I have left?" |

## Tools

Claude picks the tools from your request. You do not call them by name.

Hunter asks you to confirm before it starts a sequence, pushes leads to a CRM, or deletes a sequence. It also asks before it adds recipients to a sequence that is already in progress.

Data Platform plans have no Discover or Sequences tools. `Find-Similar-Companies` is not on the Free plan.

<!-- BEGIN GENERATED: mcp-tools:remote. Generated from the Hunter MCP server; do not edit by hand. -->

The Data column says what a tool does:

- **Reads**: changes nothing in your account.
- **Paid lookup**: looks data up for credits and saves nothing.
- **Paid, saves leads**: looks data up for credits. If the team has automatic lead saving (on by default, off on Data Platform plans), it also saves the result as a lead.
- **Writes**: changes your account.
- **Irreversible**: makes a change that cannot be undone, such as deleting data, sending emails, or pushing leads to a CRM.

### Discover

Search Hunter's company database from criteria or from a seed company. Count the contacts at each company, or list their job titles for free. Save a search and run it again later.

Try: "Find fintech companies in France with 50 to 200 employees."

| Tool | Title | Credits | Data |
|---|---|---|---|
| `Create-Saved-Search` | Create Saved Search | Free | Writes |
| `Delete-Saved-Search` | Delete Saved Search | Free | Irreversible |
| `Find-Companies` | Find Companies | Free | Reads |
| `Find-People` | Count People at Companies | Free | Reads |
| `Find-Similar-Companies` | Find Similar Companies | Free | Reads |
| `Get-Saved-Search` | Get Saved Search | Free | Reads |
| `List-Job-Titles` | List Job Titles (Free) | Free | Reads |
| `List-Saved-Searches` | List Saved Searches | Free | Reads |

### Contact data

Get the email addresses at one domain or at up to 50 domains in one call, find the email address of one person, check deliverability, and count the addresses for a domain. To pick people by job title, list them for free, then get the email addresses of the ones you choose.

Try: "Find the email address of the head of marketing at notion.com and check that it is deliverable."

| Tool | Title | Credits | Data |
|---|---|---|---|
| `Bulk-Domain-Search` | Bulk Domain Search | 1 credit per 10 emails returned for each company, rounded up | Paid lookup |
| `Domain-Search` | Domain Search | 1 credit per 10 emails returned, rounded up | Paid lookup |
| `Domain-Search-Found` | Domain Search (Found Emails Only) | 1 credit per 10 emails returned, rounded up | Paid lookup |
| `Email-Count` | Email Count | Free | Reads |
| `Email-Finder` | Email Finder | 1 credit | Paid, saves leads |
| `Email-Verifier` | Email Verifier | 0.5 credit | Paid, saves leads |
| `Preview-People` | Preview People (Free) | Free | Reads |
| `Reveal-Emails` | Reveal Emails (1 Credit Each) | 1 credit per email | Paid lookup |

### Enrichment

Get profile data for a person (from an email address) or for a company (from a domain), or both in one call.

Try: "Tell me about stripe.com."

| Tool | Title | Credits | Data |
|---|---|---|---|
| `Combined-Enrichment` | Combined Enrichment | 0.2 credit, with at least 1 credit left to start | Paid lookup |
| `Company-Enrichment` | Company Enrichment | 0.2 credit, with at least 1 credit left to start | Paid lookup |
| `Person-Enrichment` | Person Enrichment | 0.2 credit, with at least 1 credit left to start | Paid lookup |

### Leads

Read, create, update, and delete leads. Find a lead by email address. Save a company to your account by its domain.

Try: "Save these contacts as leads without overwriting existing ones."

| Tool | Title | Credits | Data |
|---|---|---|---|
| `Create-Lead` | Create Lead | Free | Writes |
| `Create-Lead-If-Missing` | Create Lead if Missing | Free | Writes |
| `Create-Or-Update-Lead` | Create or Update Lead | Free | Irreversible |
| `Delete-Lead` | Delete Lead | Free | Irreversible |
| `Get-Lead` | Get Lead | Free | Reads |
| `Lead-Exists` | Check if Lead Exists | Free | Reads |
| `List-Leads` | List Leads | Free | Reads |
| `Save-Company` | Save Company | Free | Writes |
| `Update-Lead` | Update Lead | Free | Irreversible |

### Leads lists

Manage leads lists, merge two lists, mark favorites, and put lists in folders.

Try: "Create a leads list called Q4 Outreach and add these contacts to it."

| Tool | Title | Credits | Data |
|---|---|---|---|
| `Create-Leads-List` | Create Leads List | Free | Writes |
| `Create-Leads-List-Folder` | Create Leads List Folder | Free | Writes |
| `Delete-Leads-List` | Delete Leads List | Free | Irreversible |
| `Delete-Leads-List-Folder` | Delete Leads List Folder | Free | Irreversible |
| `Favorite-Leads-List` | Favorite Leads List | Free | Writes |
| `Get-Leads-List` | Get Leads List | Free | Reads |
| `List-Leads-List-Folders` | List Leads List Folders | Free | Reads |
| `List-Leads-Lists` | List Leads Lists | Free | Reads |
| `Merge-Leads-Lists` | Merge Leads Lists | Free | Irreversible |
| `Unfavorite-Leads-List` | Unfavorite Leads List | Free | Writes |
| `Update-Leads-List` | Update Leads List | Free | Irreversible |
| `Update-Leads-List-Folder` | Update Leads List Folder | Free | Irreversible |

### Tags and custom attributes

Manage lead tags and apply them to leads. Manage the custom attributes that leads can have.

Try: "Tag these leads as priority."

| Tool | Title | Credits | Data |
|---|---|---|---|
| `Add-Tag-To-Lead` | Add Tag to Lead | Free | Writes |
| `Create-Custom-Attribute` | Create Custom Attribute | Free | Writes |
| `Create-Lead-Tag` | Create Lead Tag | Free | Writes |
| `Delete-Custom-Attribute` | Delete Custom Attribute | Free | Irreversible |
| `Delete-Lead-Tag` | Delete Lead Tag | Free | Irreversible |
| `Get-Custom-Attribute` | Get Custom Attribute | Free | Reads |
| `List-Custom-Attributes` | List Custom Attributes | Free | Reads |
| `List-Lead-Tags` | List Lead Tags | Free | Reads |
| `Remove-Tag-From-Lead` | Remove Tag from Lead | Free | Writes |
| `Update-Custom-Attribute` | Update Custom Attribute | Free | Irreversible |
| `Update-Lead-Tag` | Update Lead Tag | Free | Irreversible |

### Company lists

Manage static and dynamic company lists, add and remove companies, mark favorites, and put lists in folders.

Try: "Save these companies to a Target Accounts list."

| Tool | Title | Credits | Data |
|---|---|---|---|
| `Add-Company-To-List` | Add Company to List | Free | Writes |
| `Create-Company-List` | Create Company List | Free | Writes |
| `Create-Company-List-Folder` | Create Company List Folder | Free | Writes |
| `Delete-Company-List` | Delete Company List | Free | Irreversible |
| `Delete-Company-List-Folder` | Delete Company List Folder | Free | Irreversible |
| `Favorite-Company-List` | Favorite Company List | Free | Writes |
| `Get-Company-List` | Get Company List | Free | Reads |
| `List-Company-List-Folders` | List Company List Folders | Free | Reads |
| `List-Company-Lists` | List Company Lists | Free | Reads |
| `Remove-Company-From-List` | Remove Company from List | Free | Writes |
| `Unfavorite-Company-List` | Unfavorite Company List | Free | Writes |
| `Update-Company-List` | Update Company List | Free | Irreversible |
| `Update-Company-List-Folder` | Update Company List Folder | Free | Irreversible |

### Bulk operations

Move, copy, or delete many leads or companies in one call.

Try: "Move every lead from the Q3 list to the Q4 list."

| Tool | Title | Credits | Data |
|---|---|---|---|
| `Bulk-Copy-Companies` | Bulk Copy Companies | Free | Irreversible |
| `Bulk-Delete-Companies` | Bulk Delete Companies | Free | Irreversible |
| `Bulk-Delete-Leads` | Bulk Delete Leads | Free | Irreversible |
| `Bulk-Move-Companies` | Bulk Move Companies | Free | Irreversible |
| `Bulk-Move-Leads` | Bulk Move Leads | Free | Irreversible |

### Sequences

Create and configure email outreach sequences. Start, pause, resume, and archive them. Get open, click, and reply statistics.

Try: "Create a 3-step sequence for my Q4 Outreach list, then start it."

| Tool | Title | Credits | Data |
|---|---|---|---|
| `Archive-Sequence` | Archive Sequence | Free | Irreversible |
| `Create-Sequence` | Create Sequence | Free | Writes |
| `Delete-Sequence` | Delete Sequence | Free | Irreversible |
| `Get-Sequence` | Get Sequence | Free | Reads |
| `Get-Sequence-Stats` | Get Sequence Stats | Free | Reads |
| `List-Sequences` | List Sequences | Free | Reads |
| `Pause-Sequence` | Pause Sequence | Free | Writes |
| `Resume-Sequence` | Resume Sequence | Free | Irreversible |
| `Start-Sequence` | Start Sequence | Free | Irreversible |
|