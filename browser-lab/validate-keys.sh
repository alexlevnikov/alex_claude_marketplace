#!/usr/bin/env bash
# validate-keys.sh — prove each web-harvest cloud key actually works by making a
# real authenticated API call to each provider. Run in your Mac Terminal (which
# has your exported keys + network):
#
#     bash validate-keys.sh
#
# 2xx = key works. 401/403 = key missing/invalid/expired. Other = see the code.
# Note: the Firecrawl check performs one real scrape (costs ~1 credit).

pass=0; fail=0
ok()   { printf '  [ OK ]  %s\n' "$*"; pass=$((pass+1)); }
bad()  { printf '  [FAIL]  %s\n' "$*"; fail=$((fail+1)); }
skip() { printf '  [SKIP]  %s\n' "$*"; }

# POST/GET helper: $1=label $2=method $3=url $4=data(optional) then header args
check() {
  local label="$1" method="$2" url="$3" data="$4"; shift 4
  local hdrs=(); for h in "$@"; do hdrs+=(-H "$h"); done
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

echo "===================================================="
echo " web-harvest — API key validation"
echo "===================================================="

# --- Exa ---
if [ -n "${EXA_API_KEY:-}" ]; then
  check "Exa (api.exa.ai/search)" POST "https://api.exa.ai/search" \
    '{"query":"anthropic","numResults":1}' \
    "content-type: application/json" "x-api-key: ${EXA_API_KEY}"
else skip "Exa — EXA_API_KEY unset"; fi

# --- Tavily ---
if [ -n "${TAVILY_API_KEY:-}" ]; then
  check "Tavily (api.tavily.com/search)" POST "https://api.tavily.com/search" \
    "{\"api_key\":\"${TAVILY_API_KEY}\",\"query\":\"anthropic\",\"max_results\":1}" \
    "content-type: application/json"
else skip "Tavily — TAVILY_API_KEY unset"; fi

# --- Firecrawl (real scrape, ~1 credit) ---
if [ -n "${FIRECRAWL_API_KEY:-}" ]; then
  check "Firecrawl (api.firecrawl.dev/v2/scrape)" POST "https://api.firecrawl.dev/v2/scrape" \
    '{"url":"https://example.com"}' \
    "content-type: application/json" "Authorization: Bearer ${FIRECRAWL_API_KEY}"
else skip "Firecrawl — FIRECRAWL_API_KEY unset (optional)"; fi

# --- Bright Data ---
if [ -n "${BRIGHTDATA_API_TOKEN:-}" ]; then
  check "Bright Data (api.brightdata.com/zone/get_active_zones)" GET \
    "https://api.brightdata.com/zone/get_active_zones" "" \
    "Authorization: Bearer ${BRIGHTDATA_API_TOKEN}"
else skip "Bright Data — BRIGHTDATA_API_TOKEN unset"; fi

# --- Apify ---
if [ -n "${APIFY_TOKEN:-}" ]; then
  check "Apify (api.apify.com/v2/users/me)" GET \
    "https://api.apify.com/v2/users/me?token=${APIFY_TOKEN}" "" ""
else skip "Apify — APIFY_TOKEN unset"; fi

echo "===================================================="
echo " RESULT: ${pass} passed, ${fail} failed"
[ "$fail" = "0" ] && echo " All configured keys work." || echo " Fix the [FAIL] keys above, then re-run."
echo "===================================================="
exit "$fail"
