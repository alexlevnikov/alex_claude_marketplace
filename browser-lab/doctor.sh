#!/usr/bin/env bash
# doctor.sh — verify Browser Lab's tools are installed and available.
# Run this in the environment where your plugin's servers will run — most
# importantly, your Mac's Terminal:
#
#     bash doctor.sh
#
# It only checks/looks things up (it never launches a long-running server), so
# it always exits. Exit code 0 = all critical checks passed, 1 = something's
# missing. Cloud retrieval servers (exa/tavily/brightdata/apify) and their API
# keys are OPTIONAL — a missing key only means the web-harvest skill routes
# around that server, so those are warnings, never failures.

CRIT_FAIL=0
say()  { printf '%s\n' "$*"; }
ok()   { printf '  [ OK ]  %s\n' "$*"; }
warn() { printf '  [WARN]  %s\n' "$*"; }
fail() { printf '  [FAIL]  %s\n' "$*"; CRIT_FAIL=1; }
have() { command -v "$1" >/dev/null 2>&1; }

say "===================================================="
say " Browser Lab — environment doctor"
say " $(date)"
say "===================================================="

say ""
say "1) Runtimes"
for t in node npm npx uv uvx python3 zip unzip curl; do
  if have "$t"; then ok "$t  ($($t --version 2>&1 | head -1))"; else
    case "$t" in
      node|npm|npx) fail "$t not found  (install: brew install node)" ;;
      uv|uvx)       fail "$t not found  (install: brew install uv)" ;;
      *)            warn "$t not found" ;;
    esac
  fi
done

say ""
say "2) Browser  (required by playwright + chrome-devtools)"
CHROME=""
for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
         "/Applications/Chromium.app/Contents/MacOS/Chromium" \
         "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"; do
  [ -x "$c" ] && CHROME="$c" && break
done
if [ -z "$CHROME" ]; then
  for b in google-chrome google-chrome-stable chromium chromium-browser; do
    have "$b" && CHROME="$(command -v "$b")" && break
  done
fi
if [ -n "$CHROME" ]; then ok "Chrome/Chromium: $CHROME"
else fail "No Chrome/Chromium found  (install: brew install --cask google-chrome)"; fi

say ""
say "3) Network reachability (needed to fetch servers the first time)"
check_url() { # name url
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 "$2" 2>/dev/null)
  case "$code" in
    2*|3*) ok  "$1 reachable ($code)" ;;
    *)     fail "$1 unreachable ($code)" ;;
  esac
}
check_url "npm registry" "https://registry.npmjs.org/"
check_url "PyPI"         "https://pypi.org/simple/"

say ""
say "4) Core server packages resolvable from registries  (browser-lab skill)"
if have npm; then
  for pkg in "@playwright/mcp" "chrome-devtools-mcp" "curlconverter"; do
    v=$(npm view "$pkg" version 2>/dev/null)
    if [ -n "$v" ]; then ok "$pkg (npm $v)"; else fail "$pkg not resolvable from npm"; fi
  done
else
  fail "npm missing — cannot check npm-based servers"
fi
mv=$(curl -s --max-time 20 https://pypi.org/pypi/mitmproxy-mcp/json 2>/dev/null \
     | grep -o '"version":[[:space:]]*"[^"]*"' | head -1 | grep -o '[0-9][^"]*')
if [ -n "$mv" ]; then ok "mitmproxy-mcp (PyPI $mv)"; else fail "mitmproxy-mcp not resolvable from PyPI"; fi

say ""
say "5) Cloud retrieval servers  (web-harvest skill — all OPTIONAL)"
# Optional npm-based server
if have npm; then
  v=$(npm view "@brightdata/mcp" version 2>/dev/null)
  if [ -n "$v" ]; then ok "@brightdata/mcp (npm $v)"; else warn "@brightdata/mcp not resolvable from npm"; fi
fi
# Hosted MCP endpoints — a 2xx/3xx/4xx all prove DNS+route are fine (4xx just
# means the endpoint wants auth/a session, which is expected without a request).
check_url_opt() { # name url
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 "$2" 2>/dev/null)
  case "$code" in
    2*|3*|4*) ok   "$1 reachable ($code)" ;;
    *)        warn "$1 unreachable ($code)  (optional server)" ;;
  esac
}
check_url_opt "firecrawl (mcp.firecrawl.dev)" "https://mcp.firecrawl.dev/v2/mcp"
check_url_opt "exa (mcp.exa.ai)"              "https://mcp.exa.ai/mcp"
check_url_opt "tavily (mcp.tavily.com)"       "https://mcp.tavily.com/mcp/"
check_url_opt "apify (mcp.apify.com)"         "https://mcp.apify.com"

say ""
say "6) API keys for cloud servers  (env vars; unset = that server is skipped)"
check_key() { # label varname
  if [ -n "${!2:-}" ]; then ok "$1 set"; else warn "$1 unset  (export $2=...)"; fi
}
check_key "Exa         (EXA_API_KEY)"          EXA_API_KEY
check_key "Tavily      (TAVILY_API_KEY)"       TAVILY_API_KEY
check_key "Bright Data (BRIGHTDATA_API_TOKEN)" BRIGHTDATA_API_TOKEN
check_key "Apify       (APIFY_TOKEN)"          APIFY_TOKEN
check_key "Firecrawl   (FIRECRAWL_API_KEY, optional — unlocks crawl/extract)" FIRECRAWL_API_KEY

say ""
say "===================================================="
if [ "$CRIT_FAIL" = "0" ]; then
  say " RESULT: PASS — everything Browser Lab needs is present."
  say " (Cloud retrieval keys are optional; set the ones you'll use — see [WARN] above.)"
else
  say " RESULT: action needed — see [FAIL] lines above."
  say " Common one-time fix on macOS:"
  say "   brew install node uv"
  say "   brew install --cask google-chrome"
fi
say "===================================================="
exit "$CRIT_FAIL"
