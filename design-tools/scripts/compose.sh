#!/usr/bin/env bash
# compose.sh — shim: `bash scripts/compose.sh <tool|command …> [--task "…"] [--slug s] [--project dir] [--json]`. See compose.py.
set -euo pipefail
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/compose.py" "$@"
