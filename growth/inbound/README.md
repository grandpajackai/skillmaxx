# Inbound form acknowledgements

The `/advertise/` and `/submit/` forms post to the SkillMaxx intake worker. That worker stores the submission and does **not** send email (see `intake/worker.mjs`). FormSubmit and its `_autoresponse` field were removed in PR #88.

These templates are the approved acknowledgement copy if we later send an email ack (a Zoho filter, a routine, or a worker change):

- `autoresponse-advertise.txt` — sponsor inquiries
- `autoresponse-submit.txt` — directory submissions

They replaced the Oct 26 wording that said "No bots on this side of the inbox," which wasn't true. Brandon reads every reply; an AI assistant helps triage.

## Guard (required for any auto-reply)

Before sending an acknowledgement, load the existing thread and call `growth.outreach.lib.thread_already_has_our_reply` (or the helper in `auto_reply.py`). If Brandon or `skillmaxx@gilventures.ai` has already replied, skip. Do not stack an auto-ack on a personal reply.
