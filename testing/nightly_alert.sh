# SkillMaxx nightly failure alert. Source from bash (3.2 compatible); do not execute.
# Posts {"kind":"nightly_failure","date","step","error","log_tail"} to the Grok Bot webhook
# routine that already handles inbox alerts. Free: plain curl, no new service.
# Secrets live outside the repo in SKILLMAXX_ALERT_ENV (default ~/.skillmaxx-secrets/alert.env,
# chmod 600) as SKILLMAXX_ALERT_WEBHOOK_URL and SKILLMAXX_ALERT_WEBHOOK_KEY. They are passed to
# curl on stdin (-K -), never on the command line, and are scrubbed from the log tail.
# Every function here returns 0: an alert problem must never change the run's own result.

smx_alert_load() {
  f=${SKILLMAXX_ALERT_ENV:-$HOME/.skillmaxx-secrets/alert.env}
  if [ -z "${SKILLMAXX_ALERT_WEBHOOK_URL:-}" ] && [ -f "$f" ]; then
    set -a
    # shellcheck disable=SC1090
    . "$f" 2>/dev/null
    set +a
  fi
  return 0
}

smx_json_str() {
  # JSON string body (no quotes) for $1. Drops control characters except newline and tab.
  s=$(printf '%s' "$1" | LC_ALL=C tr -d '\000-\010\013-\037\177')
  s=${s//\\/\\\\}
  s=${s//\"/\\\"}
  s=${s//	/\\t}
  s=${s//$'\n'/\\n}
  printf '%s' "$s"
}

smx_scrub() {
  # Remove the webhook values and anything token-shaped.
  t=$1
  [ -n "${SKILLMAXX_ALERT_WEBHOOK_URL:-}" ] && t=${t//"$SKILLMAXX_ALERT_WEBHOOK_URL"/[redacted-url]}
  [ -n "${SKILLMAXX_ALERT_WEBHOOK_KEY:-}" ] && t=${t//"$SKILLMAXX_ALERT_WEBHOOK_KEY"/[redacted-key]}
  printf '%s' "$t" | sed -E \
    -e 's#(gh[pousr]_|github_pat_)[A-Za-z0-9_]{10,}#[redacted]#g' \
    -e 's#(sk|pk|rk|xox[abprs])-[A-Za-z0-9_-]{10,}#[redacted]#g' \
    -e 's#AKIA[0-9A-Z]{16}#[redacted]#g' \
    -e 's#([Bb]earer|[Tt]oken|[Aa]uthorization|[Pp]assword|[Ss]ecret|[Aa]pi[_-]?[Kk]ey)([=: ]+)[^ "]+#\1\2[redacted]#g' \
    -e 's#https?://[^/ ]*:[^@/ ]*@#https://[redacted]@#g' \
    -e 's#[A-Za-z0-9_-]{41,}#[redacted]#g'
}

# smx_alert STEP ERROR [LOGFILE] [DATE]
# Prints only "alert: http=<code>" (no URL, no key). Logs one line to $SKILLMAXX_STATE/alerts.log.
smx_alert() {
  # Tests set SKILLMAXX_ALERT_DISABLE=1: log locally, never POST to the real webhook.
  if [ "${SKILLMAXX_ALERT_DISABLE:-}" = 1 ]; then echo "alert: disabled (test) step=$1"; return 0; fi
  step=$1; err=$2; logf=${3:-}; day=${4:-$(TZ=America/New_York date +%F)}
  smx_alert_load
  tail_txt=
  if [ -n "$logf" ] && [ -f "$logf" ]; then
    tail_txt=$(tail -n "${SKILLMAXX_ALERT_TAIL_LINES:-30}" "$logf" 2>/dev/null)
  fi
  tail_txt=$(smx_scrub "$tail_txt")
  err=$(smx_scrub "$err")
  host=$(hostname -s 2>/dev/null || echo mac)
  body=$(printf '{"kind":"nightly_failure","date":"%s","step":"%s","error":"%s","log_tail":"%s","machine":"%s","at":"%s"}' \
    "$(smx_json_str "$day")" "$(smx_json_str "$step")" "$(smx_json_str "$err")" \
    "$(smx_json_str "$tail_txt")" "$(smx_json_str "$host")" "$(TZ=America/New_York date '+%F %T %Z')")
  code=000
  if [ -z "${SKILLMAXX_ALERT_WEBHOOK_URL:-}" ] || [ -z "${SKILLMAXX_ALERT_WEBHOOK_KEY:-}" ]; then
    code=noconfig
  elif ! command -v curl >/dev/null 2>&1; then
    code=nocurl
  else
    key=$SKILLMAXX_ALERT_WEBHOOK_KEY
    case "$key" in
      [Aa]uthorization:*) auth=${key#*:}; auth=${auth# } ;;
      [Bb]earer\ *) auth=$key ;;
      *) auth="Bearer $key" ;;
    esac
    code=$(printf 'url = "%s"\nheader = "Authorization: %s"\n' "$SKILLMAXX_ALERT_WEBHOOK_URL" "$auth" | \
      curl -sS -K - -o /dev/null -w '%{http_code}' -X POST \
        -H 'Content-Type: application/json' -H 'Accept: application/json' \
        --connect-timeout 10 --max-time 25 --retry 3 --retry-delay 5 --retry-all-errors \
        --data-binary "$body" 2>/dev/null) || true
    [ -n "$code" ] || code=000
  fi
  st=${SKILLMAXX_STATE:-$HOME/.local/share/skillmaxx}
  mkdir -p "$st" 2>/dev/null
  printf '%s day=%s step=%s http=%s\n' "$(TZ=America/New_York date '+%F %T %Z')" "$day" "$step" "$code" >> "$st/alerts.log" 2>/dev/null
  echo "alert: step=$step http=$code"
  return 0
}
