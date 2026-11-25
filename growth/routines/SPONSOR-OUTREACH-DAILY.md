# Routine notes: skillmaxx-daily-sponsor-outreach (weekdays ~11:00 AM ET)

**Send through the Zoho Mail API helper, not the browser.** Since 2026-11-13 (Brandon approved the API connection, t314u) all sponsor mail from skillmaxx@gilventures.ai goes through `growth/scripts/zoho_mail.py`. Do not use Zoho webmail in the box browser, and do not try box SMTP (465/587 are blocked from the box).

- Credentials: `/home/box/.skillmaxx-secrets/zoho_skillmaxx.json` (client_id, client_secret, refresh_token). Never print, copy or commit them. The helper refreshes the access token itself (cached next to the creds file, mode 600).
- Account 7217576000000008002, From `Brandon at SkillMaxx <skillmaxx@gilventures.ai>`, plain text.

## Commands

```
python3 growth/scripts/zoho_mail.py folders                 # Inbox, Spam, Sent, ... with ids
python3 growth/scripts/zoho_mail.py list Inbox --limit 30
python3 growth/scripts/zoho_mail.py list Spam
python3 growth/scripts/zoho_mail.py search "sender:example.com"
python3 growth/scripts/zoho_mail.py find example.com        # from/to/subject match in Inbox, Spam, Sent
python3 growth/scripts/zoho_mail.py content FOLDER_ID MESSAGE_ID
python3 growth/scripts/zoho_mail.py send --to a@b.com --subject "..." --body-file body.txt [--dry-run]
python3 growth/scripts/zoho_mail.py reply MESSAGE_ID --to a@b.com --subject "Re: ..." --body-file fu.txt
```

`reply` threads on an existing message (use our last Sent message in the thread, or their reply). Quote the earlier message under the new text the way webmail did.

## Every run

1. Run `python3 growth/outreach/run_day.py --date YYYY-MM-DD` from a repo checkout. It will **exit without sending** if `SKILLMAXX_POSTAL_ADDRESS` in `growth/outreach/config.env` is unset (CAN-SPAM). Only send what Brandon approved (cold pitches from an approved queue; follow-ups per OUTREACH.md §3). Window **9:00 AM–5:00 PM ET**, randomized **20–60 minutes** apart. Daily cap is 20 if any bounce landed in the previous 7 days, otherwise the ramp cap (max 30). Stop on the first non-200, and never start a second `run.py` if `/tmp/skillmaxx_outreach.lock` is held.
2. Before each recipient: `find <domain>` / `search "sender:<domain>"` across Inbox **and** Spam for any reply (mark opt-out language `opted-out` / do-not-contact); check Sent for a duplicate or a nudge already sent; for follow-ups, also read `PIPELINE.csv` status and skip `Bounced`, `opted-out` / `do-not-contact`, `declined` / `declined-warm`, `Replied`, `Lost`, and `Warm - inbound` (mailbox alone is not enough). Check the follow-up's position in the sequence and that the last touch was not too recent (`next_follow_up` wins). Skip and log anyone who fails. When sourcing a new pitch, prefer a published partnerships / sponsorships contact (or a named marketing / DevRel person on the brand's site) over `hello@` / `info@` / `sales@`. Never guess a name or address.
3. Re-check facts in the draft against the latest `src/_data/reports.json` and the live directory (counts, category names) before sending. Never invent numbers.
4. Form-lead nudges (Resend, Clerk, Sanity, Netlify, other `form` rows) are not email threads: skip them here. Also skip every `Warm - inbound` / `inbound-email` row (the prospect wrote to us) — including Autonomous (Dee, dee@autonomous.ai). Those threads are never part of the daily cold or follow-up queue; only a personal in-thread reply when there is a real reason.
5. After sending, wait a few minutes and read Inbox for bounces (`mailer-daemon`) and auto-replies; mark bounced rows **Bounced** with no follow-ups.
6. Append the one-line newsletter invite from `growth/outreach/SUBSCRIBE_PS.md` to outbound pitches, follow-ups, and polite decline replies (never on unsubscribes or opt-outs).
7. Log each send in `growth/sponsors/PIPELINE.csv` (status, date, subject, time ET, Zoho messageId, next follow-ups) and `growth/outreach/sent/YYYY-MM-DD-email-results.json`; STATUS.md line via PR + squash-merge.
