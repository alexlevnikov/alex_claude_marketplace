#!/usr/bin/env bash
# dashboard.sh — locate the design-studio dashboard (or one skill's demo) and, if asked, open it.
#
#   bash scripts/dashboard.sh               # report: where it is, size, age — open nothing
#   bash scripts/dashboard.sh --open        # open dashboard.html in the default browser
#   bash scripts/dashboard.sh --open typeset  # open demos/typeset/index.html if it exists, else the dashboard
#
# Location: $DESIGN_STUDIO_DIR, else registry/tools.json → studio.dir. Exit 1 when nothing exists.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REG="$HERE/../registry/tools.json"

OPEN=0; WANT=""
for a in "$@"; do
  case "$a" in
    --open) OPEN=1 ;;
    --*) ;;
    *) [ -n "$a" ] && WANT="$a" ;;
  esac
done

IFS=$'\t' read -r DIR DASH DEMOS REBUILD < <(python3 - "$REG" <<'PY'
import json, sys
s = json.load(open(sys.argv[1])).get("studio", {})
print("\t".join([s.get("dir", ""), s.get("dashboard", "dashboard.html"), s.get("demos", "demos"), s.get("rebuild", "")]))
PY
)
DIR="${DESIGN_STUDIO_DIR:-$DIR}"

if [ -z "$DIR" ] || [ ! -d "$DIR" ]; then
  echo "status: MISSING — design-studio directory not found"
  echo "looked: \$DESIGN_STUDIO_DIR='${DESIGN_STUDIO_DIR:-}' · registry studio.dir='$DIR'"
  echo "hint: set DESIGN_STUDIO_DIR to the design-studio checkout, or fix studio.dir in registry/tools.json"
  exit 1
fi

TARGET=""; KIND=""
if [ -n "$WANT" ]; then
  # sanitise: a skill id is [A-Za-z0-9._-]
  SAFE="$(printf '%s' "$WANT" | tr -cd 'A-Za-z0-9._-')"
  if [ -n "$SAFE" ] && [ -f "$DIR/$DEMOS/$SAFE/index.html" ]; then
    TARGET="$DIR/$DEMOS/$SAFE/index.html"; KIND="demo:$SAFE"
  else
    echo "demo: none for '$WANT' (no $DEMOS/$SAFE/index.html) — falling back to the dashboard"
  fi
fi
if [ -z "$TARGET" ]; then
  if [ -f "$DIR/$DASH" ]; then TARGET="$DIR/$DASH"; KIND="dashboard"; else
    echo "status: MISSING — $DIR/$DASH does not exist"
    echo "hint: (cd \"$DIR\" && $REBUILD) rebuilds it from candidates/skills-dashboard.json"
    exit 1
  fi
fi

SIZE="$(du -h "$TARGET" | cut -f1 | tr -d ' ')"
if stat -f %Sm -t %Y-%m-%d "$TARGET" >/dev/null 2>&1; then MOD="$(stat -f %Sm -t '%Y-%m-%d %H:%M' "$TARGET")"; else MOD="$(date -r "$TARGET" '+%Y-%m-%d %H:%M' 2>/dev/null || echo '?')"; fi
DEMO_COUNT="$(find "$DIR/$DEMOS" -mindepth 2 -maxdepth 2 -name index.html 2>/dev/null | wc -l | tr -d ' ')"

echo "status: OK   kind: $KIND"
echo "path: $TARGET"
echo "size: $SIZE   modified: $MOD   demos_on_disk: $DEMO_COUNT   rebuild: (cd \"$DIR\" && $REBUILD)"
echo "caveat: the dashboard's vendor column mis-attributes twelve ui-craft lenses to impeccable — wiki/ is authoritative"

if [ "$OPEN" = 1 ]; then
  if command -v open >/dev/null 2>&1; then open "$TARGET" && echo "opened: yes (open)"
  elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$TARGET" >/dev/null 2>&1 && echo "opened: yes (xdg-open)"
  else echo "opened: no — no 'open' or 'xdg-open' on this machine; open the path above by hand"; fi
else
  echo "opened: no (pass --open)"
fi
