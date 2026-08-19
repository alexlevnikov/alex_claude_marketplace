#!/usr/bin/env bash
# build.sh — package a plugin from this marketplace into an installable .plugin file.
#
# Shared by every plugin in the repo; lives at the marketplace root.
#
# Usage:
#   bash build.sh <plugin-dir>     # e.g. bash build.sh web-harvest
#   bash build.sh --all            # build every plugin listed in marketplace.json
#
# Output: ./<plugin-name>.plugin  (written to the marketplace root)
#
# Note: installing from this marketplace normally happens over git
# (`/plugin` → alex-claude-marketplace), which needs no .plugin file at all.
# Build one only to hand a plugin to someone out-of-band.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

usage() { echo "usage: bash build.sh <plugin-dir> | --all" >&2; exit 2; }
[ $# -ge 1 ] || usage

build_one() {
  local dir="$1"
  [ -d "$dir" ] || { echo "✖ No such plugin directory: $dir" >&2; return 1; }

  local manifest="$dir/.claude-plugin/plugin.json"
  [ -f "$manifest" ] || { echo "✖ Cannot find $manifest" >&2; return 1; }

  # Read the plugin name from the manifest (portable: no jq required).
  local name
  name="$(grep -m1 '"name"' "$manifest" 2>/dev/null \
    | sed -E 's/.*"name"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/' || true)"
  [ -n "$name" ] || { echo "✖ Could not read \"name\" from $manifest" >&2; return 1; }

  # Validate JSON if a parser is available (non-fatal skip if not).
  if command -v python3 >/dev/null 2>&1; then
    local j
    for j in "$manifest" "$dir/.mcp.json"; do
      [ -f "$j" ] || continue
      python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$j" \
        || { echo "✖ Invalid JSON: $j" >&2; return 1; }
    done
  fi

  # Every skill directory must contain a SKILL.md.
  if [ -d "$dir/skills" ]; then
    local d
    while IFS= read -r d; do
      [ -f "$d/SKILL.md" ] || { echo "✖ Missing SKILL.md in $d" >&2; return 1; }
    done < <(find "$dir/skills" -mindepth 1 -maxdepth 1 -type d)
  fi

  # No secret may ever end up inside a shipped archive.
  if grep -rIlE '(fc-|tvly-|apify_api_)[A-Za-z0-9_-]{16,}' "$dir" >/dev/null 2>&1; then
    echo "✖ Possible API key inside $dir — refusing to build." >&2
    return 1
  fi

  local out="$ROOT/${name}.plugin"
  # Build fresh in a temp file, then copy over the target: copying (rather than
  # deleting first) keeps this working where unlink is restricted, and building
  # fresh avoids stale entries in an updated-in-place archive.
  local tmp_zip="${TMPDIR:-/tmp}/${name}.$$.plugin"
  rm -f "$tmp_zip" 2>/dev/null || true
  ( cd "$dir" && zip -r "$tmp_zip" . \
      -x "*.DS_Store" \
      -x ".git/*" \
      -x "*/.git/*" \
      -x "*/.DS_Store" >/dev/null )
  cp -f "$tmp_zip" "$out"
  rm -f "$tmp_zip" 2>/dev/null || true

  printf '✔ Built %s.plugin\n  → %s\n' "$name" "$out"
  command -v du >/dev/null 2>&1 && printf '  size: %s\n' "$(du -h "$out" | cut -f1)"
}

if [ "$1" = "--all" ]; then
  # Every directory holding a plugin manifest is a plugin.
  while IFS= read -r m; do
    build_one "$(dirname "$(dirname "$m")")"
  done < <(find . -mindepth 3 -maxdepth 3 -path "./.claude-plugin/*" -prune -o \
             -name plugin.json -path "*/.claude-plugin/*" -print | sed 's|^\./||' | sort)
else
  build_one "${1%/}"
fi
