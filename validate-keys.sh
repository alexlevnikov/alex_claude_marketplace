#!/usr/bin/env bash
# validate-keys.sh — prove web-harvest's cloud keys actually work, and that they
# are stored where Claude Code can read them.
#
#     bash validate-keys.sh
#
# Two things are checked per backend, in this order:
#
#   1. SOURCE — is the key in ~/.claude/settings.json → env ?  That is the only
#      place Claude Code reads. An `export` in ~/.zshrc does NOT count: the
#      desktop app launches from the GUI and never loads a shell profile, so
#      ${EXA_API_KEY} in a .mcp.json interpolates to empty and the server 401s.
#      That was the real bug behind "exa and tavily always fail".
#
#   2. CALL — does the key authenticate against the provider's real API?
#      2xx = works. 401/403 = missing/invalid/expired.
#
# A key found only in the shell is reported as a FAIL on source even when the
# call succeeds — because the call proves the key, not the wiring.
#
# Note: the Firecrawl check performs one real scrape (costs ~1 credit).
# Key values are never printed.

SETTINGS="$HOME/.claude/settings.json"
VARS="FIRECRAWL_API_KEY EXA_API_KEY TAVILY_API_KEY BRIGHTDATA_API_TOKEN APIFY_TOKEN"

pass=0; fail=0
ok()   { printf '  [ OK ]  %s\n' "$*"; pass=$((pass+1)); }
bad()  { printf '  [FAIL]  %s\n' "$*"; fail=$((fail+1)); }
note() { printf '  [INFO]  %s\n' "$*"; }
skip() { printf '  [SKIP]  %s\n' "$*"; }

echo "===================================================="
echo " web-harvest — key source + live validation"
echo " source of truth: $SETTINGS  → env"
echo "===================================================="
echo ""
echo "1) Source check — is the key where Claude Code reads it?"

if ! command -v python3 >/dev/null 2>&1; then
  echo "  python3 is required to read $SETTINGS" >&2
  exit 2
fi

# Load the settings.json values into SETTINGS_<VAR> shell variables. Values are
# shell-quoted by python and never printed.
eval "$(python3 - "$SETTINGS" $VARS <<'PY'
import json, shlex, sys
path, names = sys.argv[1], sys.argv[2:]
try:
    env = json.load(open(path)).get("env") or {}
except Exception:
    env = {}
for n in names:
    print("SETTINGS_%s=%s" % (n, shlex.quote(str(env.get(n, "")).strip())))
PY
)"

for var in $VARS; do
  sval_name="SETTINGS_$var"
  sval="${!sval_name}"
  shellval="${!var:-}"
  if [ -n "$sval" ]; then
    ok "$var — in settings.json env"
  elif [ -n "$shellval" ]; then
    bad "$var — only exported in this shell; Claude Code will NOT see it. Copy it into $SETTINGS → env."
  else
    skip "$var — not set anywhere"
  fi
  # The live call below prefers the settings.json value; fall back to the shell
  # one so a mis-stored-but-valid key is still reported honestly.
  eval "USE_$var=\${sval:-\$shellval}"
done

echo ""
echo "2) Live call — does the key authenticate?"

# check: $1=label $2=method $3=url $4=data(may be empty) then header args
check() {
  local label="$1" method="$2" url="$3" data="$4"; shift 4
  local hdrs=(); local h
  for h in "$@"; do [ -n "$h" ] && hdrs+=(-H "$h"); done
  local code
  if [ "$method" = "GET" ]; then
    code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 30 "${hdrs[@]}" "$url")
  else
    code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 30 -X "$method" "${hdrs[@]}" -d "$data" "$url")
  fi
  case "$code" in
    2*)      ok  "$label  (HTTP $code)";;
    401|403) bad "$label  (HTTP $code — key missing/invalid)";;
    *)       bad "$label  (HTTP $code — unexpected; check service/endpoint)";;
  esac
}

# --- Exa ---
if [ -n "${USE_EXA_API_KEY:-}" ]; then
  check "Exa         (api.exa.ai/search)" POST "https://api.exa.ai/search" \
    '{"query":"anthropic","numResults":1}' \
    "content-type: application/json" "x-api-key: ${USE_EXA_API_KEY}"
else skip "Exa — no key"; fi

# --- Tavily ---
if [ -n "${USE_TAVILY_API_KEY:-}" ]; then
  check "Tavily      (api.tavily.com/search)" POST "https://api.tavily.com/search" \
    "{\"query\":\"anthropic\",\"max_results\":1}" \
    "content-type: application/json" "Authorization: Bearer ${USE_TAVILY_API_KEY}"
else skip "Tavily — no key"; fi

# --- Firecrawl (real scrape, ~1 credit) ---
if [ -n "${USE_FIRECRAWL_API_KEY:-}" ]; then
  check "Firecrawl   (api.firecrawl.dev/v2/scrape)" POST "https://api.firecrawl.dev/v2/scrape" \
    '{"url":"https://example.com"}' \
    "content-type: application/json" "Authorization: Bearer ${USE_FIRECRAWL_API_KEY}"
else note "Firecrawl — no key; the keyless tier still serves Search/Scrape/Parse"; fi

# --- Bright Data ---
if [ -n "${USE_BRIGHTDATA_API_TOKEN:-}" ]; then
  check "Bright Data (api.brightdata.com/zone/get_active_zones)" GET \
    "https://api.brightdata.com/zone/get_active_zones" "" \
    "Authorization: Bearer ${USE_BRIGHTDATA_API_TOKEN}"
else skip "Bright Data — no key"; fi

# --- Apify ---
if [ -n "${USE_APIFY_TOKEN:-}" ]; then
  check "Apify       (api.apify.com/v2/users/me)" GET \
    "https://api.apify.com/v2/users/me" "" \
    "Authorization: Bearer ${USE_APIFY_TOKEN}"
else skip "Apify — no key"; fi

echo ""
echo "3) Repo hygiene — no key may ever be committed"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1; then
  hits=$(git -C "$REPO" grep -InE '(fc-|tvly-|apify_api_)[A-Za-z0-9_-]{16,}' -- . 2>/dev/null | head -5)
  if [ -n "$hits" ]; then
    bad "possible key material tracked in git:"
    printf '%s\n' "$hits" | sed 's/^/          /'
  else
    ok "no key-shaped strings tracked in git"
  fi
else
  skip "not a git repo — hygiene check skipped"
fi

echo ""
echo "===================================================="
echo " RESULT: ${pass} passed, ${fail} failed"
if [ "$fail" = "0" ]; then
  echo " Every configured key is stored correctly and works."
else
  echo " Fix the [FAIL] lines above, restart Claude Code, then re-run."
fi
echo "===================================================="
exit "$fail"
