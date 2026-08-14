#!/usr/bin/env bash
# build.sh — package the browser-lab plugin source into an installable .plugin file.
#
# Usage:
#   bash build.sh          # from anywhere; resolves its own location
#   ./build.sh             # if you've run: chmod +x build.sh
#
# Output: ../<plugin-name>.plugin  (written next to this source folder)
set -euo pipefail

# Resolve this script's own directory = the plugin source root, so it works
# no matter what directory you call it from.
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SRC_DIR"

MANIFEST=".claude-plugin/plugin.json"
if [ ! -f "$MANIFEST" ]; then
  echo "✖ Cannot find $MANIFEST — run this from inside the plugin source folder." >&2
  exit 1
fi

# Read the plugin name from the manifest (portable: no jq/python required).
NAME="$(grep -m1 '"name"' "$MANIFEST" 2>/dev/null \
  | sed -E 's/.*"name"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/' || true)"
if [ -z "$NAME" ]; then
  echo "✖ Could not read \"name\" from $MANIFEST" >&2
  exit 1
fi

OUT="../${NAME}.plugin"

# Validate JSON if a parser is available (non-fatal skip if not).
if command -v python3 >/dev/null 2>&1; then
  for j in "$MANIFEST" ".mcp.json"; do
    [ -f "$j" ] || continue
    python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$j" \
      || { echo "✖ Invalid JSON: $j" >&2; exit 1; }
  done
fi

# Every skill directory must contain a SKILL.md.
if [ -d skills ]; then
  while IFS= read -r d; do
    [ -f "$d/SKILL.md" ] || { echo "✖ Missing SKILL.md in $d" >&2; exit 1; }
  done < <(find skills -mindepth 1 -maxdepth 1 -type d)
fi

# Build a fresh temp archive, then copy it over the target. Copying (rather
# than deleting first) keeps this working even where unlink is restricted, and
# building fresh avoids leaving stale entries in an updated-in-place archive.
TMP_ZIP="${TMPDIR:-/tmp}/${NAME}.$$.plugin"
rm -f "$TMP_ZIP" 2>/dev/null || true
zip -r "$TMP_ZIP" . \
  -x "build.sh" \
  -x "doctor.sh" \
  -x "*.DS_Store" \
  -x ".git/*" \
  -x "*/.git/*" \
  -x "*/.DS_Store" >/dev/null
cp -f "$TMP_ZIP" "$OUT"
rm -f "$TMP_ZIP" 2>/dev/null || true

OUT_ABS="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"
echo "✔ Built ${NAME}.plugin"
echo "  → $OUT_ABS"
command -v du >/dev/null 2>&1 && echo "  size: $(du -h "$OUT" | cut -f1)"
echo ""
echo "To install/update: open the Cowork desktop app and add this .plugin file."
