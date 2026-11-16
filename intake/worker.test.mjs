import assert from "node:assert/strict";
import test from "node:test";
import { isAccepted } from "../src/assets/intake-contract.js";
import { handle } from "./worker.mjs";

class MemKV {
  constructor() { this.store = new Map(); }
  async get(key) { return this.store.has(key) ? this.store.get(key) : null; }
  async put(key, value) { this.store.set(key, String(value)); }
  async delete(key) { this.store.delete(key); }
  async list({ prefix }) {
    return { keys: [...this.store.keys()].filter((key) => key.startsWith(prefix)).map((name) => ({ name })) };
  }
}

function body(fields = {}, extra = {}) {
  return {
    kind: "skill",
    openedAt: Date.now() - 5000,
    page: "/submit/",
    fax_number: "",
    fields: { name: "Example skill", source_url: "https://example.com/skill", ...fields },
    ...extra,
  };
}

function post(payload, origin = "http://127.0.0.1:8080", ip = "203.0.113.9") {
  return new Request("https://intake.example/intake", {
    method: "POST",
    headers: { "content-type": "application/json", origin, "cf-connecting-ip": ip },
    body: JSON.stringify(payload),
  });
}

test("stores a valid skill and acknowledges only after the write", async () => {
  const kv = new MemKV();
  const env = { INTAKE: kv, INTAKE_READ_TOKEN: "test-token-not-a-secret" };
  const res = await handle(post(body()), env);
  const json = await res.json();
  assert.equal(res.status, 200);
  assert.equal(isAccepted(res.status, json), true);
  const stored = JSON.parse(kv.store.get(`sub:${json.id}`));
  assert.equal(stored.fields.name, "Example skill");
  assert.equal(stored.fields.source_url, "https://example.com/skill");
  assert.equal(JSON.stringify(stored).includes("203.0.113.9"), false);
  const health = await handle(new Request("https://intake.example/health"));
  const healthBody = await health.json();
  assert.equal(healthBody.received, false);
  assert.equal(isAccepted(health.status, healthBody), false);
});

test("a honeypot or missing storage does not acknowledge receipt", async () => {
  const kv = new MemKV();
  const spam = await handle(post(body({}, { fax_number: "filled" })), { INTAKE: kv, INTAKE_READ_TOKEN: "t" });
  assert.equal((await spam.json()).received, false);
  assert.equal(kv.store.size, 0);
  const down = await handle(post(body()), {});
  const downBody = await down.json();
  assert.equal(down.status, 503);
  assert.equal(downBody.received, false);
  assert.equal(isAccepted(down.status, downBody), false);
});

test("a failed write is not reported as received", async () => {
  const kv = new MemKV();
  kv.put = async (key, value) => {
    if (String(key).startsWith("sub:")) throw new Error("kv down");
    kv.store.set(key, String(value));
  };
  const res = await handle(post(body()), { INTAKE: kv, INTAKE_READ_TOKEN: "t" });
  const json = await res.json();
  assert.equal(res.status, 503);
  assert.equal(json.error, "storage");
  assert.equal(isAccepted(res.status, json), false);
});

test("rate limit and foreign origins are refused", async () => {
  const kv = new MemKV();
  const env = { INTAKE: kv, INTAKE_READ_TOKEN: "t" };
  let last = 200;
  for (let i = 0; i < 9; i++) {
    const res = await handle(post(body()), env);
    last = res.status;
  }
  assert.equal(last, 429);
  const evil = await handle(post(body(), "https://evil.example"), env);
  assert.equal(evil.status, 403);
  const bare = await handle(new Request("https://intake.example/intake", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body()),
  }), env);
  assert.equal(bare.status, 403);
});

test("inbox requires the read token and can delete one record", async () => {
  const kv = new MemKV();
  const env = { INTAKE: kv, INTAKE_READ_TOKEN: "owner-token" };
  const created = await (await handle(post(body()), env)).json();
  const hidden = await handle(new Request("https://intake.example/inbox"), env);
  assert.equal(hidden.status, 401);
  const noTokenEnv = await handle(new Request("https://intake.example/inbox"), { INTAKE: kv });
  assert.equal(noTokenEnv.status, 404);
  const listed = await handle(new Request("https://intake.example/inbox", {
    headers: { authorization: "Bearer owner-token" },
  }), env);
  const inbox = await listed.json();
  assert.equal(inbox.submissions.length, 1);
  assert.equal(inbox.submissions[0].id, created.id);
  assert.equal(inbox.received, false);
  const removed = await handle(new Request(`https://intake.example/inbox?id=${created.id}`, {
    method: "DELETE",
    headers: { authorization: "Bearer owner-token" },
  }), env);
  assert.equal((await removed.json()).deleted, true);
  assert.equal(kv.store.has(`sub:${created.id}`), false);
});

test("preflight allows the site and local tests only", async () => {
  const ok = await handle(new Request("https://intake.example/intake", {
    method: "OPTIONS",
    headers: { origin: "https://skillmaxx.gilventures.ai" },
  }));
  assert.equal(ok.status, 204);
  assert.equal(ok.headers.get("access-control-allow-origin"), "https://skillmaxx.gilventures.ai");
  const no = await handle(new Request("https://intake.example/intake", {
    method: "OPTIONS",
    headers: { origin: "https://evil.example" },
  }));
  assert.equal(no.status, 403);
});
