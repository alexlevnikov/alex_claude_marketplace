#!/usr/bin/env bash
# discover.sh — shim: `bash scripts/discover.sh "<task>" [--top N] [--json]`. See discover.py.
set -euo pipefail
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/discover.py" "$@"
