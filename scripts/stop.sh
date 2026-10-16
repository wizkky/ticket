#!/usr/bin/env bash
set -euo pipefail
source "$(dirname -- "$0")/common.sh"
exec python3 "$CAUDAL_ROOT/scripts/stop.py"
