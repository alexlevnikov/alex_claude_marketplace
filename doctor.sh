#!/usr/bin/env bash
# doctor.sh — verify this marketplace's plugins have what they need.
# Shared by every plugin; lives at the marketplace root. Run it in your Mac
# Terminal:
#
#     bash doctor.sh
#
# It only checks and looks things up (it never launches a long-running server),
# so it always exits. Exit code 0 = all critical checks passed, 1 = something is
# missing.
#
# Critical  = browser-lab's local stdio core (node, uv, Chrome, the packages).
# Warning   = web-harvest's cloud backends and their keys — a missing key only
#             means the skill routes around that backend.
#
# This checks that keys are *reachable by Claude Code*, i.e. present in
# ~/.claude/settings.json → env. Exports in ~/.zshrc do NOT count: the desktop
# app launches from the GUI and never reads a shell profile. To prove a key
# actually works, run: bash validate-keys.sh

CRIT_FAIL=0
SETTINGS="$HOME/.claude/settings.json"
say()  { printf '%s\n' "$*"; }
ok()   { printf '  [ OK ]  %s\n' "$*"; }
warn() { printf '  [WARN]  %s\n' "$*"; }
fail() { printf '  [FAIL]  %s\n' "$*"; CRIT_FAIL=1; }
have() { command -v "$1" >/dev/null 2>&1; }

say "===================================================="
say " alex-claude-marketplace — environment doctor"
say " $(date)"
say "===================================================="

say ""
say "1) Runtimes  (browser-lab)"
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
say "2) Browser  (browser-lab: playwright + chrome-devtools)"
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
say "3) Registry reachability  (needed to fetch the stdio servers first time)"
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
say "4) browser-lab server packages resolvable"
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
say "5) web-harvest endpoints  (all hosted http — 0 local processes)"
# 2xx/3xx/4xx all prove DNS + route are fine; 4xx just means the endpoint wants
# auth or a session, which is expected without a real MCP request.
check_url_opt() { # name url
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 "$2" 2>/dev/null)
  case "$code" in
    2*|3*|4*) ok   "$1 reachable ($code)" ;;
    *)        warn "$1 unreachable ($code)" ;;
  esac
}
check_url_opt "firecrawl  (mcp.firecrawl.dev)"  "https://mcp.firecrawl.dev/v2/mcp"
check_url_opt "exa        (mcp.exa.ai)"         "https://mcp.exa.ai/mcp"
check_url_opt "tavily     (mcp.tavily.com)"     "https://mcp.tavily.com/mcp/"
check_url_opt "brightdata (mcp.brightdata.com)" "https://mcp.brightdata.com/mcp"
check_url_opt "apify      (mcp.apify.com)"      "https://mcp.apify.com"

say ""
say "6) Keys where Claude Code can actually read them  ($SETTINGS → env)"
if [ ! -f "$SETTINGS" ]; then
  warn "$SETTINGS does not exist — no keys are reachable by Claude Code"
elif ! have python3; then
  warn "python3 missing — cannot parse $SETTINGS"
else
  for var in FIRECRAWL_API_KEY EXA_API_KEY TAVILY_API_KEY BRIGHTDATA_API_TOKEN APIFY_TOKEN; do
    # Prints only presence, never the value.
    state=$(python3 - "$SETTINGS" "$var" <<'PY'
import json,sys
try:
    env = json.load(open(sys.argv[1])).get("env") or {}
except Exception as e:
    print("unparseable"); sys.exit()
print("set" if str(env.get(sys.argv[2], "")).strip() else "missing")
PY
)
    case "$state" in
      set)         ok   "$var in settings.json env" ;;
      unparseable) warn "$var — could not parse $SETTINGS" ;;
      *)
        if [ -n "${!var:-}" ]; then
          warn "$var is exported in this shell but NOT in settings.json — Claude Code will 401. Copy it into $SETTINGS → env."
        else
          warn "$var not set  (add it to $SETTINGS → env)"
        fi ;;
    esac
  done
fi

say ""
say "7) What this actually costs right now"
if have ps; then
  ps -Ao rss=,command= 2>/dev/null | grep -Ei "mcp|npm exec" | grep -v grep \
    | awk '{s+=$1} END {printf "  %.0f MB resident across %d MCP-ish processes\n", s/1024, NR}'
  say "  (browser-lab accounts for 3 stdio servers per open session; web-harvest for 0)"
fi

say ""
say "===================================================="
if [ "$CRIT_FAIL" = "0" ]; then
  say " RESULT: PASS — browser-lab has everything it needs."
  say " web-harvest keys are optional per backend; see [WARN] lines above,"
  say " then prove them for real with:  bash validate-keys.sh"
else
  say " RESULT: action needed — see [FAIL] lines above."
  say " Common one-time fix on macOS:"
  say "   brew install node uv"
  say "   brew install --cask google-chrome"
fi
say "===================================================="
exit "$CRIT_FAIL"
