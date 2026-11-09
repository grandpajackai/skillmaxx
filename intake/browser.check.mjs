/** MOCKED browser checks. fetch is intercepted. Nothing is delivered to Cloudflare,
 * email, or a real inbox. A "Received" screen in this file is a fake acknowledgement
 * used to prove the page refuses to say received for any weaker response. */
import { spawn } from "node:child_process";
import { mkdirSync } from "node:fs";
import { createRequire } from "node:module";
import assert from "node:assert/strict";
import { after, before, test } from "node:test";
import { chromium } from "playwright";

const require = createRequire(import.meta.url);
const axePath = require.resolve("axe-core/axe.js");
const OUT = "/opt/cursor/artifacts";
const MOCK_ID = "smx_mocked" + "0".repeat(18);
const PORT = 8765;
const BASE = `http://127.0.0.1:${PORT}`;
mkdirSync(OUT, { recursive: true });

let server;
let browser;

function cors(route) {
  return {
    "access-control-allow-origin": BASE,
    "access-control-allow-methods": "POST, OPTIONS",
    "access-control-allow-headers": "content-type, accept",
  };
}

async function waitForServer() {
  for (let i = 0; i < 50; i++) {
    try {
      const res = await fetch(`${BASE}/submit/`);
      if (res.ok) return;
    } catch { /* retry */ }
    await new Promise((r) => setTimeout(r, 100));
  }
  throw new Error("local site did not start");
}

async function axe(page, selector) {
  await page.addScriptTag({ path: axePath });
  return page.evaluate(async (root) => {
    const result = await window.axe.run(document.querySelector(root), { runOnly: ["wcag2a", "wcag2aa"] });
    return result.violations.map((v) => ({ id: v.id, impact: v.impact, targets: v.nodes.slice(0, 3).map((n) => n.target.join(" ")) }));
  }, selector);
}

function assertNoSerious(violations, where) {
  const bad = violations.filter((v) => v.impact === "serious" || v.impact === "critical");
  assert.deepEqual(bad, [], `${where} accessibility: ${JSON.stringify(bad)}`);
}

async function overflow(page) {
  return page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
}

before(async () => {
  server = spawn("python3", ["-m", "http.server", String(PORT), "--bind", "127.0.0.1"], { cwd: "_site", stdio: "ignore" });
  await waitForServer();
  browser = await chromium.launch();
});

after(async () => {
  await browser?.close();
  server?.kill();
});

test("phone submit form is short, keyboardable, and does not pretend to send", async () => {
  const page = await browser.newPage({ viewport: { width: 390, height: 844 }, permissions: ["clipboard-read", "clipboard-write"] });
  const posts = [];
  page.on("request", (req) => { if (req.method() === "POST") posts.push(req.url()); });
  const errors = [];
  page.on("pageerror", (err) => errors.push(err.message));
  await page.goto(`${BASE}/submit/?sent=true`);
  assert.equal(await page.locator("#submit-form").isVisible(), true, "a ?sent=true query must not hide the form");
  assert.equal(await page.locator("#submit-ok h2").count(), 0);
  assert.equal((await page.locator("#submit-form button").textContent()).trim(), "Copy details");
  assert.match(await page.locator("#intake-note").innerText(), /does not send/);
  assert.equal(await page.locator("#skill-email").isVisible(), false, "optional email stays collapsed");
  assert.ok((await overflow(page)) <= 1, "390px page overflows");
  await page.screenshot({ path: `${OUT}/submit-phone-390.png` });
  assertNoSerious(await axe(page, "#form-card"), "submit");

  await page.setViewportSize({ width: 320, height: 700 });
  assert.ok((await overflow(page)) <= 1, "320px page overflows");
  await page.setViewportSize({ width: 390, height: 844 });

  await page.locator("#skill-name").focus();
  await page.keyboard.press("Tab");
  assert.equal(await page.evaluate(() => document.activeElement.id), "skill-url");
  await page.keyboard.press("Tab");
  assert.equal(await page.evaluate(() => document.activeElement.tagName), "SUMMARY");
  await page.keyboard.press("Tab");
  assert.equal(await page.evaluate(() => document.activeElement.tagName), "BUTTON");
  await page.keyboard.press("Enter");
  await page.locator("#submit-err.is-on").waitFor();
  assert.match(await page.locator("#submit-err").innerText(), /Nothing was sent/);
  assert.equal(await page.evaluate(() => document.activeElement.id), "skill-name");
  assert.equal(await page.locator("#skill-name").getAttribute("aria-invalid"), "true");
  await page.screenshot({ path: `${OUT}/submit-validation-phone.png` });

  await page.locator("#skill-name").fill("Example skill");
  await page.locator("#skill-url").fill("https://example.com/skill");
  const before = page.url();
  await page.locator("#submit-form button").click();
  await page.locator("#submit-ok h2").waitFor();
  assert.equal((await page.locator("#submit-ok h2").innerText()).trim(), "Copied");
  assert.match(await page.locator("#submit-ok").innerText(), /Not sent/);
  assert.doesNotMatch(await page.locator("#submit-ok").innerText(), /Received/);
  const clip = await page.evaluate(() => navigator.clipboard.readText());
  assert.match(clip, /Not sent automatically/);
  assert.match(clip, /Example skill/);
  assert.equal(await page.locator("#skill-name").getAttribute("aria-invalid"), null);
  assert.equal(posts.length, 0, "copy mode must not POST");
  assert.equal(page.url(), before, "copy mode must not navigate");
  assert.equal(new URL(page.url()).search, "", "a ?sent=true query must not stick");
  await page.locator("#submit-ok").scrollIntoViewIfNeeded();
  await page.locator("#form-card").screenshot({ path: `${OUT}/submit-copied-not-sent.png` });
  assert.deepEqual(errors, []);
  await page.close();
});

test("mocked direct submit: duplicate clicks, a bare 200, and a real acknowledgement shape", async () => {
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  let posts = 0;
  let mode = "ack";
  await page.route("**/intake", async (route) => {
    if (route.request().method() === "OPTIONS") {
      await route.fulfill({ status: 204, headers: cors() });
      return;
    }
    posts += 1;
    if (mode === "abort") { await route.abort("failed"); return; }
    const body = JSON.parse(route.request().postData() || "{}");
    assert.equal(body.kind, "skill");
    assert.equal(body.fax_number, "");
    if (mode === "bare") {
      await route.fulfill({ status: 200, contentType: "application/json", headers: cors(), body: JSON.stringify({ success: true }) });
      return;
    }
    await new Promise((r) => setTimeout(r, 400));
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      headers: cors(),
      body: JSON.stringify({ ok: true, received: true, id: MOCK_ID }),
    });
  });
  await page.goto(`${BASE}/submit/`);
  await page.locator("#submit-form").evaluate((form) => {
    form.dataset.endpoint = "http://127.0.0.1:9/intake";
    const btn = form.querySelector("button");
    btn.textContent = "Submit skill";
    btn.dataset.label = "Submit skill";
    form.querySelector(".hint").textContent = "Nothing is marked received unless the inbox confirms it.";
  });
  await page.locator("#intake-note").evaluate((el) => {
    el.textContent = "The button stays on this page. A confirmation appears only after the inbox confirms it stored your submission. This screen is a mocked inbox response, not a live delivery.";
  });
  await page.locator("#skill-name").fill("Example skill");
  await page.locator("#skill-url").fill("https://example.com/skill");
  await page.evaluate(() => {
    const form = document.querySelector("#submit-form");
    form.requestSubmit();
    form.requestSubmit();
  });
  await page.locator("#submit-ok h2", { hasText: "Received" }).waitFor();
  assert.equal(posts, 1, "a second submit while the first is in flight must be ignored");
  assert.match(await page.locator("#submit-ok").innerText(), new RegExp(MOCK_ID));
  assert.equal(await page.locator("#submit-form").isVisible(), false);
  await page.screenshot({ path: `${OUT}/submit-received-mocked.png` });

  mode = "bare";
  posts = 0;
  await page.goto(`${BASE}/submit/`);
  await page.locator("#submit-form").evaluate((form) => {
    form.dataset.endpoint = "http://127.0.0.1:9/intake";
    const btn = form.querySelector("button");
    btn.textContent = "Submit skill";
    btn.dataset.label = "Submit skill";
    form.querySelector(".hint").textContent = "Nothing is marked received unless the inbox confirms it.";
  });
  await page.locator("#intake-note").evaluate((el) => {
    el.textContent = "The button stays on this page. A confirmation appears only after the inbox confirms it stored your submission.";
  });
  await page.locator("#skill-name").fill("Example skill");
  await page.locator("#skill-url").fill("https://example.com/skill");
  await page.locator("#submit-form button").click();
  await page.locator("#submit-err.is-on").waitFor();
  assert.match(await page.locator("#submit-err").innerText(), /Nothing was marked received/);
  assert.equal(await page.locator("#submit-ok h2").count(), 0);
  assert.equal(await page.locator("#submit-form").isVisible(), true);
  assert.equal(await page.locator("#submit-form button").isEnabled(), true);
  await page.screenshot({ path: `${OUT}/submit-bare-200-not-received.png` });

  mode = "abort";
  const postsBeforeAbort = posts;
  await page.locator("#submit-form button").click();
  await page.waitForFunction(() => (document.querySelector("#submit-err")?.textContent || "").includes("didn't finish"));
  assert.ok(posts > postsBeforeAbort, "the failed request was actually sent");
  assert.match(await page.locator("#submit-err").innerText(), /didn't finish/);
  assert.equal(await page.locator("#submit-form button").isEnabled(), true);
  await page.close();
});

test("advertise and sponsor-thanks forms stay short and payment links stay put", async () => {
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await page.goto(`${BASE}/advertise/`);
  const html = await page.content();
  for (const url of [
    "https://buy.stripe.com/5kQ00jgPG7LCfRr8rn8g000",
    "https://buy.stripe.com/eVq00jdDu9TK48J5fb8g008",
    "https://buy.stripe.com/eVq5kDdDuaXO8oZ0YV8g001",
    "https://buy.stripe.com/4gM14nczq7LCfRr3738g004",
    "https://buy.stripe.com/3cI28rfLCgi8cFfgXT8g002",
    "https://buy.stripe.com/3cI9AT42U9TKcFfgXT8g005",
    "https://buy.stripe.com/8x2cN52YQaXO8oZ8rn8g003",
    "https://buy.stripe.com/00w5kDari1ne6gR4b78g006",
    "https://billing.stripe.com/p/login/5kQ00jgPG7LCfRr8rn8g000",
  ]) assert.ok(html.includes(url), url);
  assert.equal(await page.locator("#ad-name").isVisible(), false);
  assert.equal(await page.locator("#ad-email").isVisible(), true);
  assert.ok((await overflow(page)) <= 1, "advertise overflows at 390px");
  await page.locator("#inquiry-form").scrollIntoViewIfNeeded();
  await page.locator("#inquiry-form").screenshot({ path: `${OUT}/advertise-form-phone.png` });
  assertNoSerious(await axe(page, "#inquiry-form"), "advertise");
  await page.locator("#ad-form button").click();
  await page.locator("#ad-error.is-on").waitFor();
  assert.match(await page.locator("#ad-error").innerText(), /Nothing was sent/);

  await page.goto(`${BASE}/sponsor/thanks/?slot=featured-monthly`);
  assert.equal(await page.locator("#sp-slot").inputValue(), "Featured slot");
  assert.equal(await page.locator("#sp-plan").inputValue(), "monthly");
  assert.equal(await page.locator("#sp-name").isVisible(), false);
  assert.equal(await page.locator("#sp-link").isVisible(), true);
  assert.equal((await page.content()).includes("buy.stripe.com"), false);
  assert.match(await page.locator("body").innerText(), /does not charge you again/);
  assert.match(await page.locator("body").innerText(), /receipt comes from the payment provider/);
  assert.ok((await overflow(page)) <= 1, "thanks overflows at 390px");
  await page.locator("#intake").screenshot({ path: `${OUT}/thanks-form-phone.png` });
  assertNoSerious(await axe(page, "#intake"), "thanks");
  await page.locator("#sp-email").focus();
  await page.keyboard.press("Tab");
  assert.equal(await page.evaluate(() => document.activeElement.id), "sp-slot");
  await page.keyboard.press("Tab");
  assert.equal(await page.evaluate(() => document.activeElement.id), "sp-link");
  await page.close();
});
