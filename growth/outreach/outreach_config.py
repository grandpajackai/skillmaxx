"""Load the SkillMaxx outreach config. No secrets live here."""
from __future__ import annotations

import os
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "config.env"

MISSING_POSTAL_MESSAGE = (
    "Refusing to send: SKILLMAXX_POSTAL_ADDRESS is unset. "
    "Add a Brandon-approved postal address to growth/outreach/config.env "
    "(CAN-SPAM requires a physical address on commercial email). "
    "Outreach is held until then."
)


def parse_env_file(path: Path) -> dict[str, str]:
    vals: dict[str, str] = {}
    if not path.is_file():
        return vals
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        vals[key.strip()] = value.strip().strip('"').strip("'")
    return vals


def postal_address() -> str:
    """Return the approved postal address, or '' if unset."""
    if "SKILLMAXX_POSTAL_ADDRESS" in os.environ:
        return (os.environ.get("SKILLMAXX_POSTAL_ADDRESS") or "").strip()
    cfg = os.environ.get("SKILLMAXX_OUTREACH_CONFIG")
    path = Path(cfg) if cfg else CONFIG_PATH
    return parse_env_file(path).get("SKILLMAXX_POSTAL_ADDRESS", "").strip()


def require_postal_address() -> str:
    addr = postal_address()
    if not addr:
        raise SystemExit(MISSING_POSTAL_MESSAGE)
    return addr
