/** Shared rules for SkillMaxx forms and the intake worker.
 * A response is accepted only when it matches isAccepted(). HTTP 200 is not enough. */

export const TO = "skillmaxx@gilventures.ai";
export const MIN_OPEN_MS = 800;
export const MAX_OPEN_MS = 24 * 60 * 60 * 1000;
export const MAX_BODY_BYTES = 12000;

const CATEGORIES = [
  "automation", "communication", "database", "deployment", "design", "development",
  "education & research", "mcp servers", "monitoring", "productivity", "security",
  "utilities", "other",
];

const AD_TYPES = [
  "Custom / other",
  "Newsletter sponsor ($19 for 1 issue founding)",
  "Newsletter 4-pack ($59/mo for 4 issues founding)",
  "Featured slot ($29 for 1 month founding)",
  "Category sponsor ($15 for 1 month founding)",
  "Founding bundle ($49 for 1 month, worth $63)",
];

const SLOTS = ["Newsletter sponsor", "Featured slot", "Category sponsor", "Founding bundle"];

export const SCHEMAS = {
  skill: {
    subject: (f) => `Skill submission: ${f.name}`,
    required: ["name", "source_url"],
    fields: {
      name: { max: 120 },
      source_url: { max: 400, url: true },
      email: { max: 200, email: true },
      description: { max: 200, newlines: true },
      category: { max: 40, enum: CATEGORIES },
      install_claude_code: { max: 400, url: true },
      install_codex: { max: 400, url: true },
      install_grok_build: { max: 400, url: true },
      install_cursor: { max: 400, url: true },
      install_pi: { max: 400, url: true },
    },
  },
  "sponsor-inquiry": {
    subject: (f) => `Sponsor inquiry: ${f.ad_type}`,
    required: ["email", "ad_type"],
    fields: {
      email: { max: 200, email: true },
      ad_type: { max: 160, enum: AD_TYPES },
      name: { max: 120 },
      company: { max: 160 },
      message: { max: 2000, newlines: true },
    },
  },
  "sponsor-assets": {
    subject: (f) => `Sponsor assets: ${f.slot}`,
    required: ["email", "slot", "link", "ad_copy"],
    fields: {
      email: { max: 200, email: true },
      slot: { max: 80, enum: SLOTS },
      link: { max: 400, url: true },
      ad_copy: { max: 400, newlines: true },
      name: { max: 120 },
      company: { max: 160 },
      start_date: { max: 10, date: true },
      logo_url: { max: 400, url: true },
      category: { max: 80 },
      plan: { max: 16, enum: ["once", "monthly"] },
    },
  },
};

function isHttpUrl(value) {
  let u;
  try { u = new URL(value); } catch { return false; }
  if (u.protocol !== "http:" && u.protocol !== "https:") return false;
  if (u.username || u.password) return false;
  if (!u.hostname || u.hostname.length > 253) return false;
  return true;
}

function isEmail(value) {
  return value.length <= 200 && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

export function validateFields(kind, fields) {
  const schema = SCHEMAS[kind];
  if (!schema) return { ok: false, error: "kind", field: "kind" };
  if (!fields || typeof fields !== "object" || Array.isArray(fields)) {
    return { ok: false, error: "type", field: "fields" };
  }
  for (const key of Object.keys(fields)) {
    if (!Object.prototype.hasOwnProperty.call(schema.fields, key)) {
      return { ok: false, error: "field", field: key };
    }
  }
  const value = {};
  for (const [key, rule] of Object.entries(schema.fields)) {
    const raw = fields[key];
    if (raw == null || (typeof raw === "string" && raw.trim() === "")) {
      if (schema.required.includes(key)) return { ok: false, error: "required", field: key };
      continue;
    }
    if (typeof raw !== "string") return { ok: false, error: "type", field: key };
    const v = raw.trim();
    if (v.length > rule.max) return { ok: false, error: "length", field: key };
    if (v.includes("\0")) return { ok: false, error: "type", field: key };
    if (!rule.newlines && /[\r\n]/.test(v)) return { ok: false, error: "type", field: key };
    if (rule.enum && !rule.enum.includes(v)) return { ok: false, error: "enum", field: key };
    if (rule.url && !isHttpUrl(v)) return { ok: false, error: "url", field: key };
    if (rule.email && !isEmail(v)) return { ok: false, error: "email", field: key };
    if (rule.date) {
      if (!/^\d{4}-\d{2}-\d{2}$/.test(v) || Number.isNaN(Date.parse(`${v}T00:00:00Z`))) {
        return { ok: false, error: "date", field: key };
      }
    }
    value[key] = rule.email ? v.toLowerCase() : v;
  }
  return { ok: true, value, subject: schema.subject(value) };
}

export function validateSubmission(body, now = Date.now()) {
  if (!body || typeof body !== "object" || Array.isArray(body)) return { ok: false, error: "type" };
  if (typeof body.fax_number === "string" && body.fax_number.trim()) return { ok: false, error: "rejected" };
  if (typeof body.openedAt !== "number" || !Number.isFinite(body.openedAt)) return { ok: false, error: "timing" };
  const age = now - body.openedAt;
  if (age < MIN_OPEN_MS || age > MAX_OPEN_MS) return { ok: false, error: "timing" };
  let page = "";
  if (body.page != null && body.page !== "") {
    if (typeof body.page !== "string" || !/^\/[a-z0-9/_-]{0,80}$/.test(body.page)) {
      return { ok: false, error: "page" };
    }
    page = body.page;
  }
  const fields = validateFields(body.kind, body.fields);
  if (!fields.ok) return fields;
  return { ok: true, kind: body.kind, page, value: fields.value, subject: fields.subject };
}

/** True only for an explicit inbox acknowledgement. A bare 200 is not acceptance. */
export function isAccepted(status, body) {
  if (typeof status !== "number" || status < 200 || status >= 300) return false;
  if (!body || typeof body !== "object" || Array.isArray(body)) return false;
  if (body.ok !== true || body.received !== true) return false;
  return typeof body.id === "string" && /^smx_[a-z0-9]{16,}$/.test(body.id);
}

export function copyText(kind, fields) {
  const checked = validateFields(kind, fields);
  if (!checked.ok) return checked;
  const lines = Object.entries(checked.value).map(([k, v]) => `${k.replace(/_/g, " ")}: ${v}`);
  const text = [
    `To: ${TO}`,
    `Subject: ${checked.subject}`,
    "",
    lines.join("\n"),
    "",
    "Not sent automatically. Paste this into mail you are already signed in to.",
  ].join("\n");
  return { ok: true, text, subject: checked.subject };
}

/** Empty means direct delivery is off. A bad value fails the build instead of shipping a broken URL. */
export function endpointOk(raw) {
  const v = String(raw || "").trim();
  if (!v) return "";
  let u;
  try { u = new URL(v); } catch { throw new Error("INTAKE_ENDPOINT is not a URL"); }
  if (u.protocol !== "https:") throw new Error("INTAKE_ENDPOINT must use https");
  if (u.username || u.password) throw new Error("INTAKE_ENDPOINT must not include credentials");
  if (u.search || u.hash) throw new Error("INTAKE_ENDPOINT must not include a query or hash");
  const path = u.pathname.replace(/\/$/, "");
  if (!path.endsWith("/intake")) throw new Error("INTAKE_ENDPOINT must end in /intake");
  return u.origin + path;
}
