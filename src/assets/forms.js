/** On-page form behavior. Direct delivery runs only when data-endpoint is set.
 * Success is shown only after isAccepted(). Copy mode never says the note was sent. */
import { copyText, isAccepted, validateFields } from "./intake-contract.js";

const MESSAGES = {
  required: "Add the required fields. Nothing was sent.",
  email: "Check the email address. Nothing was sent.",
  url: "Use a full http or https link. Nothing was sent.",
  length: "One of the fields is too long. Nothing was sent.",
  enum: "Choose one of the listed options. Nothing was sent.",
  date: "Use a real date. Nothing was sent.",
  type: "Check the form fields. Nothing was sent.",
  field: "That form couldn't be read. Nothing was sent.",
  kind: "This form is misconfigured. Nothing was sent.",
  timing: "Wait a moment and try again. Nothing was received.",
  rejected: "That didn't go through. Nothing was received.",
  page: "This page couldn't be verified. Nothing was received.",
  rate: "Too many attempts from this network. Nothing was received.",
  unconfigured: "The inbox isn't turned on. Nothing was received.",
  storage: "The inbox couldn't store that. Nothing was received.",
  timeout: "No confirmation came back. Nothing was marked received.",
  network: "The request didn't finish. Nothing was received.",
  bad_response: "The response was not a confirmation. Nothing was marked received.",
  origin: "This page isn't allowed to submit. Nothing was received.",
};

const openedAt = Date.now();

function message(code) {
  return MESSAGES[code] || MESSAGES.bad_response;
}

function collect(form) {
  const fields = {};
  let fax = "";
  for (const el of form.elements) {
    if (!el.name || el.type === "submit" || el.type === "button") continue;
    if (el.name === "fax_number") { fax = el.value || ""; continue; }
    const value = String(el.value || "").trim();
    if (value) fields[el.name] = value;
  }
  return { fields, fax };
}

function fieldEl(form, name) {
  return name ? form.elements.namedItem(name) : null;
}

function showError(form, err, text, field) {
  const ok = form.dataset.ok && document.querySelector(form.dataset.ok);
  if (!text) {
    if (err) { err.textContent = ""; err.classList.remove("is-on"); }
    return;
  }
  if (ok) { ok.classList.remove("is-on"); ok.replaceChildren(); }
  if (!err) return;
  err.textContent = text;
  err.classList.add("is-on");
  const el = fieldEl(form, field);
  for (const input of form.elements) {
    if (input.name && input.type !== "submit") input.removeAttribute("aria-invalid");
  }
  if (el && el.focus) {
    el.setAttribute("aria-invalid", "true");
    el.focus();
  } else err.focus();
}

function showStatus(ok, title, detail, extra) {
  if (!ok) return;
  ok.classList.add("is-on");
  ok.replaceChildren();
  const h = document.createElement("h2");
  h.textContent = title;
  const p = document.createElement("p");
  p.textContent = detail;
  ok.append(h, p);
  if (extra) ok.append(extra);
  ok.focus();
}

function showManualCopy(ok, text) {
  const area = document.createElement("textarea");
  area.value = text;
  area.readOnly = true;
  area.rows = 8;
  area.setAttribute("aria-label", "Submission text, not sent");
  showStatus(ok, "Not sent", "Copy failed. Select this text and paste it into mail you are already signed in to. This was not sent.", area);
  area.focus();
  area.select();
}

function release(form, btn, label) {
  form.dataset.busy = "";
  form.removeAttribute("aria-busy");
  if (btn) { btn.disabled = false; btn.textContent = label; }
}

async function onSubmit(form, event) {
  event.preventDefault();
  if (form.dataset.busy === "1") return;
  const btn = form.querySelector('button[type="submit"]');
  const label = btn ? (btn.dataset.label || btn.textContent) : "";
  const err = form.dataset.err && document.querySelector(form.dataset.err);
  const ok = form.dataset.ok && document.querySelector(form.dataset.ok);
  const kind = form.dataset.kind;
  form.dataset.busy = "1";
  form.setAttribute("aria-busy", "true");
  if (btn) { btn.disabled = true; btn.textContent = form.dataset.endpoint ? "Sending…" : "Copying…"; }

  const { fields, fax } = collect(form);
  const checked = validateFields(kind, fields);
  if (!checked.ok || fax.trim()) {
    release(form, btn, label);
    showError(form, err, fax.trim() ? message("rejected") : message(checked.error), checked.field);
    return;
  }
  for (const input of form.elements) {
    if (input.removeAttribute) input.removeAttribute("aria-invalid");
  }

  const endpoint = (form.dataset.endpoint || "").trim();
  if (!endpoint) {
    const copied = copyText(kind, fields);
    try {
      if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error("no clipboard");
      await navigator.clipboard.writeText(copied.text);
      showError(form, err, "", "");
      showStatus(ok, "Copied", "Not sent. Paste it into an email to skillmaxx@gilventures.ai from an account you are already signed in to. This page did not open an email app.");
    } catch {
      showError(form, err, "", "");
      showManualCopy(ok, copied.text);
    }
    release(form, btn, label);
    return;
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 20000);
  let accepted = false;
  try {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "content-type": "application/json", accept: "application/json" },
      body: JSON.stringify({ kind, openedAt, page: location.pathname, fax_number: fax, fields }),
      signal: controller.signal,
      credentials: "omit",
      cache: "no-store",
      mode: "cors",
    });
    const text = await res.text();
    let parsed = null;
    try { parsed = JSON.parse(text); } catch { parsed = null; }
    if (!isAccepted(res.status, parsed)) {
      const code = parsed && typeof parsed.error === "string" ? parsed.error : "bad_response";
      showError(form, err, message(code), parsed && parsed.field);
      return;
    }
    accepted = true;
    showError(form, err, "", "");
    showStatus(ok, "Received", `Reference ${parsed.id}. The inbox confirmed it stored this. This page says received only after that confirmation.`);
    form.hidden = true;
  } catch (error) {
    showError(form, err, error && error.name === "AbortError" ? message("timeout") : message("network"));
  } finally {
    clearTimeout(timer);
    if (!accepted) release(form, btn, label);
  }
}

function init(form) {
  const btn = form.querySelector('button[type="submit"]');
  if (btn) btn.dataset.label = btn.textContent.trim();
  form.addEventListener("submit", (event) => { onSubmit(form, event); });
}

for (const form of document.querySelectorAll("form.intake")) init(form);

const stale = new URL(location.href);
if (stale.searchParams.has("sent")) {
  stale.searchParams.delete("sent");
  history.replaceState(null, "", stale.pathname + stale.search + stale.hash);
}

window.addEventListener("pageshow", () => {
  for (const form of document.querySelectorAll("form.intake")) {
    if (form.hidden) continue;
    const btn = form.querySelector('button[type="submit"]');
    release(form, btn, btn && (btn.dataset.label || btn.textContent));
  }
});
