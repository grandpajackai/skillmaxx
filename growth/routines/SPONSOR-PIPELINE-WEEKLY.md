# Routine: weekly sponsor pipeline (Mondays)

**Schedule intent:** Monday ~9:00 AM America/New_York (weekday only).  
**Budget:** $0. **Never send** email/DM without a Brandon-approved batch.

## Prompt (for UpdateRoutine)

Check the SkillMaxx sponsor sales pipeline and only ping Brandon when a decision or batch approval is needed.

1. Read growth/sponsors/PIPELINE.csv and growth/sponsors/OUTREACH.md in repo grandpajackai/skillmaxx (master).
2. Check Stripe (Gil Ventures live) for new successful Payment Link checkouts and active SkillMaxx subscriptions since the last run; if any, log them in growth/sponsors/PIPELINE.md bookings table and start fulfillment per growth/sponsors/PLAYBOOK.md.
3. Count prospects by status (Target / Contacted / Replied / Booked / Live / Lost). Note founding sponsors booked out of 10.
4. Check whether newsletter issue #2 has been sent and approximate Beehiiv subscriber count vs the 25-subscriber outreach gate.
5. For Contacted rows: if 7 days since last_touch with no reply, draft Follow-up 1; if 14 days, draft Follow-up 2 then mark Lost/Nurture. Send follow-ups autonomously under OUTREACH.md (day 7 / day 14), then stop; ping Brandon only on replies/bookings/problems.
6. If the gate is open and fewer than 2 new Contacted this week: draft the next batch of up to 5 Target emails (top of PIPELINE.csv) into growth/outreach/batch-YYYY-MM-DD.md using OUTREACH.md templates, refresh live install numbers from /reports/, and ask Brandon in this chat for one yes/no on the whole batch. Do not send until he approves.
7. Near BFCM (Nov 24–Dec 1 ET): include remaining BFCM inventory (Category/Newsletter 12-mo lock; Featured Dec $19 one slot) and only mention BFCM to leads who already Replied.
8. Update the Sales pipeline section on the SkillMaxx owner dashboard Page if counts changed.

Deliver the result to Brandon in this chat. If nothing moved and no batch is ready, send one short "pipeline quiet" line (or skip if he has asked for silence on no-ops).

Never invent emails. Never touch Stripe payouts, refunds, bank, or settings. Never post or email sponsors without an approved batch.
