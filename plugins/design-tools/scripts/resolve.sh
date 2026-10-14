#!/usr/bin/env bash
# resolve.sh — shim: `bash scripts/resolve.sh <tool> [--json]` / `--all`. See resolve.py for the search order.
set -euo pipefail
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/resolve.py" "$@"
