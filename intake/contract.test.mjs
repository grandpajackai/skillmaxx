import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { copyText, endpointOk, isAccepted, validateFields, validateSubmission } from "../src/assets/intake-contract.js";

const skill = { name: "Example skill", source_url: "https://example.com/skill" };

test("accepts only an explicit inbox acknowledgement", () => {
  const id = "smx_" + "a".repeat(24);
  assert.equal(isAccepted(200, { success: true }), false);
  assert.equal(isAccepted(200, { ok: true }), false);
  assert.equal(isAccepted(200, { ok: true, received: true }), false);
  assert.equal(isAccepted(200, { ok: true, received: true, id: "smx_short" }), false);
  assert.equal(isAccepted(200, { ok: true, received: false, id }), false);
  assert.equal(isAccepted(500, { ok: true, received: true, id }), false);
  assert.equal(isAccepted(200, null), false);
  assert.equal(isAccepted(200, "ok"), false);
  assert.equal(isAccepted(201, { ok: true, received: true, id }), true);
});

test("skill form requires name and source url only", () => {
  assert.equal(validateFields("skill", skill).ok, true);
  const missing = validateFields("skill", { name: "Example skill" });
  assert.equal(missing.ok, false);
  assert.equal(missing.error, "required");
  assert.equal(missing.field, "source_url");
  assert.equal(validateFields("skill", { ...skill, source_url: "javascript:alert(1)" }).error, "url");
  assert.equal(validateFields("skill", { ...skill, email: "not-an-email" }).error, "email");
  assert.equal(validateFields("skill", { ...skill, email: "Ada@Example.com" }).value.email, "ada@example.com");
  assert.equal(validateFields("skill", { ...skill, bonus: "nope" }).error, "field");
});

test("submission rejects a filled honeypot and an instant post", () => {
  const now = 1_700_000_000_000;
  const base = { kind: "skill", page: "/submit/", fields: skill, openedAt: now - 5000 };
  assert.equal(validateSubmission(base, now).ok, true);
  assert.equal(validateSubmission({ ...base, fax_number: "https://spam.example" }, now).error, "rejected");
  assert.equal(validateSubmission({ ...base, openedAt: now }, now).error, "timing");
  assert.equal(validateSubmission({ ...base, page: "/submit/?email=secret@example.com" }, now).error, "page");
});

test("copy text is explicitly not a delivery", () => {
  const copied = copyText("skill", skill);
  assert.equal(copied.ok, true);
  assert.match(copied.text, /Not sent automatically/);
  assert.doesNotMatch(copied.text, /Inquiry sent|Submission received|Assets received/);
});

test("endpoint config fails closed on a bad url", () => {
  assert.equal(endpointOk(""), "");
  assert.equal(endpointOk("https://skillmaxx.example/intake"), "https://skillmaxx.example/intake");
  assert.throws(() => endpointOk("http://skillmaxx.example/intake"), /https/);
  assert.throws(() => endpointOk("https://user:pass@skillmaxx.example/intake"), /credentials/);
  assert.throws(() => endpointOk("https://skillmaxx.example/intake?x=1"), /query/);
});

test("shipped forms do not claim a send or open GitHub", () => {
  const submit = readFileSync(new URL("../src/submit.njk", import.meta.url), "utf8");
  const advertise = readFileSync(new URL("../src/advertise.njk", import.meta.url), "utf8");
  const thanks = readFileSync(new URL("../src/sponsor/thanks.njk", import.meta.url), "utf8");
  for (const src of [submit, advertise, thanks]) {
    assert.doesNotMatch(src, /formsubmit|data-smx-form|Inquiry sent|Submission received|Assets received|sent=true|issues\/new/i);
  }
  assert.doesNotMatch(submit, /mailto:/i);
  assert.match(advertise, /href="\{\{ t\.url \}\}"/);
  assert.match(advertise, /href="\{\{ t\.subUrl \}\}"/);
  assert.match(advertise, /sponsorLinks\.portalUrl/);
  const links = JSON.parse(readFileSync(new URL("../src/_data/sponsorLinks.json", import.meta.url), "utf8"));
  const urls = links.slots.flatMap((slot) => [slot.url, slot.subUrl]);
  assert.deepEqual(urls, [
    "https://buy.stripe.com/5kQ00jgPG7LCfRr8rn8g000",
    "https://buy.stripe.com/eVq00jdDu9TK48J5fb8g008",
    "https://buy.stripe.com/eVq5kDdDuaXO8oZ0YV8g001",
    "https://buy.stripe.com/4gM14nczq7LCfRr3738g004",
    "https://buy.stripe.com/3cI28rfLCgi8cFfgXT8g002",
    "https://buy.stripe.com/3cI9AT42U9TKcFfgXT8g005",
    "https://buy.stripe.com/8x2cN52YQaXO8oZ8rn8g003",
    "https://buy.stripe.com/00w5kDari1ne6gR4b78g006",
  ]);
  assert.equal(links.portalUrl, "https://billing.stripe.com/p/login/5kQ00jgPG7LCfRr8rn8g000");
});
