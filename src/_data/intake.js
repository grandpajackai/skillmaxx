import { endpointOk } from "../assets/intake-contract.js";

const endpoint = endpointOk(process.env.INTAKE_ENDPOINT || "");
const enabled = Boolean(endpoint);

export default {
  endpoint,
  enabled,
  skillButton: enabled ? "Submit skill" : "Copy details",
  inquiryButton: enabled ? "Send inquiry" : "Copy details",
  assetsButton: enabled ? "Send assets" : "Copy details",
  note: enabled
    ? "The button stays on this page. A confirmation appears only after the inbox confirms it stored your submission."
    : "Direct delivery is not turned on yet. Copy details stays on this page. It does not send, and it does not open an email app or a GitHub login.",
  help: enabled
    ? "Nothing is marked received unless the inbox confirms it."
    : "Copies a note you can paste into mail you are already signed in to. Nothing is sent from this page.",
};
