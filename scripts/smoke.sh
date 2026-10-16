#!/usr/bin/env bash
set -euo pipefail
source "$(dirname -- "$0")/common.sh"
cd "$CAUDAL_ROOT"
uv run --no-project --python "$CAUDAL_ROOT/apps/api/.venv/bin/python" \
  --with pyzbar==0.1.9 --with pillow==12.3.0 python scripts/smoke.py "$@"
