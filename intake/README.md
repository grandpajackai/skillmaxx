# SkillMaxx intake

Direct form delivery is **off** until this worker is deployed and `INTAKE_ENDPOINT` is set. The site then posts JSON to `POST /intake`. The page says "Received" only when the response is HTTP 2xx **and** the body is `{ "ok": true, "received": true, "id": "smx_…" }`. A bare 200 is treated as failure.

The worker stores the submission in Workers KV. It does not send email. Visitor text is not written to the public repo, a public GitHub issue, or the client.

## Smallest setup

Do this only if signup stays on the free plan and does not ask for a card. Limits below are from Cloudflare's docs as checked on 2026-11-09.

1. Create a free Cloudflare account. Workers Free is the default plan: $0, 100,000 requests/day, 10 ms CPU per request ([pricing](https://developers.cloudflare.com/workers/platform/pricing/), [limits](https://developers.cloudflare.com/workers/platform/limits/)). Included KV: 100,000 reads/day, 1,000 writes/day, 1,000 list operations/day, 1 GB ([KV pricing](https://developers.cloudflare.com/kv/platform/pricing/)).
2. From this directory, `npx wrangler login` (or an API token with Workers and KV edit). Do not commit the token.
3. `npx wrangler kv namespace create INTAKE`. Uncomment the `[[kv_namespaces]]` block in `wrangler.toml` and paste the id.
4. `npx wrangler secret put INTAKE_READ_TOKEN`. Use a long random value. Do not commit it. This token reads and deletes inbox entries.
5. `npx wrangler deploy`. The URL is `https://skillmaxx-intake.<your-subdomain>.workers.dev`. This does **not** move `gilventures.ai` DNS, so Zoho mail stays where it is.
6. `GET /health` should return `{ "ok": true, "received": false, "storage": true }`. `received: false` is deliberate: health is not a submission.
7. In the GitHub repo settings, add an Actions **variable** (not a secret) `INTAKE_ENDPOINT` = `https://skillmaxx-intake.<your-subdomain>.workers.dev/intake`. The next Pages deploy turns the buttons into Submit / Send. Until that variable exists, the buttons say "Copy details" and do not post.
8. Submit once from a phone on the live site. The page must show `Reference smx_…`. Then `curl` (or a browser) `GET /inbox` with `Authorization: Bearer <token>` and confirm that same id is stored. Delete the test with `DELETE /inbox?id=smx_…` and the same header.

## Limits that matter

- `workers.dev` needs no custom domain. Cloudflare's docs say that hostname is for personal or hobby projects, not business-critical production, and Browser Integrity Check can block some non-browser clients with error 1010 before the worker runs ([workers.dev](https://developers.cloudflare.com/workers/configuration/routing/workers-dev/)). A normal browser submit is the check that counts. A custom domain would put the zone on Cloudflare; do not change `gilventures.ai` nameservers for this, because Zoho MX is there.
- About 8 accepted posts per IP per hour. Writes over the free KV daily cap fail closed (`received: false`), they do not show a confirmation.
- Spam controls are a honeypot, a short minimum fill time, field checks, and that rate limit. There is no captcha service.
- The inbox is not emailed. Read it with the bearer token. Success on the page means KV accepted the write, not that a person has seen it.

## Not production

`node --test intake/contract.test.mjs intake/worker.test.mjs` uses an in-memory KV. `node intake/browser.check.mjs` mocks `fetch`. Neither contacts Cloudflare or sends mail.
