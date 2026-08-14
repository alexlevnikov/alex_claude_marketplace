#!/usr/bin/env bash
# setup-keys.sh — securely store Browser Lab's cloud API keys and wire them into
# your shell so Claude Code inherits them. Run in your Mac Terminal:
#
#     bash setup-keys.sh
#
# It writes keys to  ~/.browser-lab-keys.env  (chmod 600, OUTSIDE this git repo,
# so a key can never be committed) and adds one `source` line to your shell
# profile. Keys are read silently (never shown, never saved to shell history).
# Re-run any time — existing values are preserved unless you type a new one.
#
# Compatible with macOS stock bash 3.2 (no associative arrays / bash-4 features).
#
# After running: restart Claude Code, then `bash validate-keys.sh` to prove them.

set -euo pipefail

SECRETS="$HOME/.browser-lab-keys.env"

# Pick the profile the interactive shell actually loads.
case "${SHELL##*/}" in
  zsh)  PROFILE="$HOME/.zshrc" ;;
  bash) PROFILE="$HOME/.bashrc" ;;
  *)    PROFILE="$HOME/.profile" ;;
esac

# var name | provider | where to get it | example prefix
KEYS=(
  "FIRECRAWL_API_KEY|Firecrawl (optional — unlocks crawl/extract)|firecrawl.dev|fc-..."
  "EXA_API_KEY|Exa (neural/semantic search)|exa.ai|(no prefix)"
  "TAVILY_API_KEY|Tavily (fast factual search)|tavily.com|tvly-..."
  "BRIGHTDATA_API_TOKEN|Bright Data (anti-bot unblocking, datasets)|brightdata.com|(no prefix)"
  "APIFY_TOKEN|Apify (store actors, large runs)|apify.com|apify_api_..."
)

echo "===================================================="
echo " Browser Lab — cloud API key setup"
echo " Secrets file: $SECRETS"
echo " Shell profile: $PROFILE"
echo "===================================================="
echo " All keys are OPTIONAL. Press Enter to skip one (or keep its current"
echo " value). Input is hidden. Free tiers exist on every provider."
echo ""

# Load existing values so a re-run can preserve them (sets each var in-shell).
if [ -f "$SECRETS" ]; then
  # shellcheck disable=SC1090
  source "$SECRETS"
fi

# Start the new secrets file in a temp file with tight permissions.
umask 077
tmp="$(mktemp "${SECRETS}.XXXXXX")"
{
  echo "# Browser Lab cloud API keys — sourced by $PROFILE. Do NOT commit."
  echo "# Regenerate with browser-lab/setup-keys.sh. $(date)"
} > "$tmp"

count=0
for entry in "${KEYS[@]}"; do
  IFS='|' read -r var label site example <<< "$entry"
  existing="${!var:-}"                       # bash 3.2 indirect expansion
  if [ -n "$existing" ]; then
    state="currently set — Enter keeps it"
  else
    state="unset"
  fi
  printf '%s\n  get at: %s   e.g. %s   [%s]\n  %s = ' \
    "$label" "$site" "$example" "$state" "$var"
  IFS= read -rs value || true                # silent read; -r keeps backslashes
  echo                                        # newline after hidden input

  # Decide the final value: new input wins, else keep existing, else skip.
  final=""
  if [ -n "$value" ]; then
    final="$value"
  elif [ -n "$existing" ]; then
    final="$existing"
  fi

  if [ -n "$final" ]; then
    printf -v quoted '%q' "$final"            # safe-escape for re-sourcing
    printf 'export %s=%s\n' "$var" "$quoted" >> "$tmp"
    count=$((count + 1))
  fi
done

mv "$tmp" "$SECRETS"
chmod 600 "$SECRETS"

# Wire the secrets file into the shell profile (exactly once).
if ! grep -Fq "$SECRETS" "$PROFILE" 2>/dev/null; then
  printf '\n[ -f "%s" ] && source "%s"   # Browser Lab keys\n' "$SECRETS" "$SECRETS" >> "$PROFILE"
  echo ""
  echo "  Added source line to $PROFILE"
else
  echo ""
  echo "  $PROFILE already sources the secrets file — left as is."
fi

echo ""
echo "===================================================="
echo " Stored $count key(s) in $SECRETS (chmod 600)."
echo " Next:"
echo "   1) source \"$PROFILE\"        # load keys into THIS terminal"
echo "   2) restart Claude Code        # so its MCP servers inherit them"
echo "   3) bash validate-keys.sh      # prove each key works"
echo "===================================================="
