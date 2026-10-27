# One-off routine: BFCM banner (offer APPROVED 2026-10-27)

Banner copy (approved; no money/test-result line; no free Dec line):
"Black Friday, our way: book a Category or Newsletter founding slot by Cyber Monday and lock your rate for 12 months (not 6). Featured: $19 for December — one slot."

## Run 1 — Fri Nov 27, 2026, 9:00 AM ET
1. Verify /advertise/ shows the date-gated banner (already merged; client gate).
2. In Stripe Dashboard → Product catalog → Coupons / Promotion codes: set `BFCM-FEATURED-DEC` **active** if it was left inactive (code `promo_1UV6cVHnNCwlg7U0W6J8ttqW`, coupon `bfcm_featured_dec`). Featured one-time Payment Link already has `allow_promotion_codes`.
3. Log STATUS.md. No BFCM social posts unless separately approved.

## Run 2 — Mon Dec 1, 2026, 9:00 AM ET
1. Remove `#bfcm` block via PR after client gate hides it.
2. PIPELINE.md: tag Category/Newsletter BFCM bookings with 12-month lock; note Featured Dec $19 if redeemed.

No Stripe payout/refund/bank changes.
