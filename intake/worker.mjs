/** SkillMaxx intake. Stores a validated submission in Workers KV and acknowledges
 * it only after that write resolves. No email is sent from here. */
import { MAX_BODY_BYTES, validateSubmission } from "../src/assets/intake-contract.js";

const SITE_ORIGIN = "https://skillmaxx.gilventures.ai";
const RATE_PER_HOUR = 8;

function originAllowed(origin) {
  if (!origin) return false;
  if (origin === SITE_ORIGIN) return true;
  try {
    const u = new URL(origin);
    return u.protocol === "http:" && (u.hostname === "127.0.0.1" || u.hostname === "localhost");
  } catch {
    return false;
  }
}

function corsHeaders(origin) {
  if (!originAllowed(origin)) return null;
  return {
    "access-control-allow-origin": origin,
    "access-control-allow-methods": "POST, OPTIONS",
    "access-control-allow-headers": "content-type, accept",
    "access-control-max-age": "86400",
    vary: "Origin",
  };
}

function json(status, body, cors) {
  const headers = { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" };
  if (cors) Object.assign(headers, cors);
  return new Response(JSON.stringify(body), { status, headers });
}

function safeEqual(a, b) {
  const enc = new TextEncoder();
  const x = enc.encode(String(a));
  const y = enc.encode(String(b));
  if (x.length !== y.length) return false;
  let diff = 0;
  for (let i = 0; i < x.length; i++) diff |= x[i] ^ y[i];
  return diff === 0;
}

function authorized(request, env) {
  const token = env.INTAKE_READ_TOKEN || "";
  if (!token) return false;
  const header = request.headers.get("authorization") || "";
  const match = /^Bearer\s+(\S+)$/.exec(header);
  if (!match) return false;
  return safeEqual(match[1], token);
}

async function sha256(value) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function newId() {
  const bytes = new Uint8Array(12);
  crypto.getRandomValues(bytes);
  let hex = "";
  for (const b of bytes) hex += b.toString(16).padStart(2, "0");
  return `smx_${hex}`;
}

async function rateOk(env, request) {
  const ip = request.headers.get("cf-connecting-ip") || "0";
  const hour = new Date().toISOString().slice(0, 13);
  const pepper = env.INTAKE_READ_TOKEN || "skillmaxx-intake";
  const hash = (await sha256(`${pepper}|${ip}`)).slice(0, 32);
  const key = `rl:${hour}:${hash}`;
  const prev = Number((await env.INTAKE.get(key)) || "0");
  if (prev >= RATE_PER_HOUR) return false;
  await env.INTAKE.put(key, String(prev + 1), { expirationTtl: 60 * 60 * 2 });
  return true;
}

async function readInbox(env, id) {
  if (id) {
    if (!/^smx_[a-z0-9]{16,}$/.test(id)) return json(400, { ok: false, received: false, error: "id" });
    const raw = await env.INTAKE.get(`sub:${id}`);
    if (!raw) return json(404, { ok: false, received: false, error: "not_found" });
    return json(200, { ok: true, received: false, submission: JSON.parse(raw) });
  }
  const listed = await env.INTAKE.list({ prefix: "sub:", limit: 50 });
  const submissions = [];
  for (const key of listed.keys) {
    const raw = await env.INTAKE.get(key.name);
    if (!raw) continue;
    try { submissions.push(JSON.parse(raw)); } catch { /* skip a corrupt value */ }
  }
  submissions.sort((a, b) => String(b.receivedAt).localeCompare(String(a.receivedAt)));
  return json(200, { ok: true, received: false, submissions });
}

export async function handle(request, env = {}) {
  const url = new URL(request.url);
  const origin = request.headers.get("origin");
  const cors = corsHeaders(origin);

  if (request.method === "OPTIONS") {
    if (!cors) return new Response(null, { status: 403 });
    return new Response(null, { status: 204, headers: cors });
  }

  if (request.method === "GET" && url.pathname === "/health") {
    return json(200, { ok: true, received: false, storage: Boolean(env.INTAKE) });
  }

  if (url.pathname === "/inbox" && (request.method === "GET" || request.method === "DELETE")) {
    if (!env.INTAKE_READ_TOKEN) return json(404, { ok: false, received: false, error: "not_found" });
    if (!authorized(request, env)) return json(401, { ok: false, received: false, error: "unauthorized" });
    if (!env.INTAKE) return json(503, { ok: false, received: false, error: "unconfigured" });
    const id = url.searchParams.get("id") || "";
    if (request.method === "DELETE") {
      if (!/^smx_[a-z0-9]{16,}$/.test(id)) return json(400, { ok: false, received: false, error: "id" });
      await env.INTAKE.delete(`sub:${id}`);
      return json(200, { ok: true, received: false, deleted: true, id });
    }
    return readInbox(env, id);
  }

  if (request.method !== "POST" || url.pathname !== "/intake") {
    return json(404, { ok: false, received: false, error: "not_found" }, cors);
  }
  if (!cors) return json(403, { ok: false, received: false, error: "origin" });

  const type = (request.headers.get("content-type") || "").toLowerCase();
  if (!type.includes("application/json")) return json(415, { ok: false, received: false, error: "type" }, cors);
  const text = await request.text();
  if (text.length > MAX_BODY_BYTES) return json(413, { ok: false, received: false, error: "length" }, cors);
  let body;
  try { body = JSON.parse(text); } catch { return json(400, { ok: false, received: false, error: "type" }, cors); }

  const result = validateSubmission(body);
  if (!result.ok) {
    return json(400, { ok: false, received: false, error: result.error, field: result.field || "" }, cors);
  }
  if (!env.INTAKE) return json(503, { ok: false, received: false, error: "unconfigured" }, cors);

  let allowed = false;
  try { allowed = await rateOk(env, request); } catch { return json(503, { ok: false, received: false, error: "storage" }, cors); }
  if (!allowed) return json(429, { ok: false, received: false, error: "rate" }, cors);

  const id = newId();
  const record = {
    id,
    kind: result.kind,
    receivedAt: new Date().toISOString(),
    page: result.page,
    fields: result.value,
  };
  try {
    await env.INTAKE.put(`sub:${id}`, JSON.stringify(record));
  } catch {
    return json(503, { ok: false, received: false, error: "storage" }, cors);
  }
  return json(200, { ok: true, received: true, id }, cors);
}

export default { fetch: handle };
