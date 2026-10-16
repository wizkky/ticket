#!/usr/bin/env bash
set -euo pipefail
source "$(dirname -- "$0")/common.sh"
cd "$CAUDAL_ROOT"
if [[ ! -f .local/stack.env || ! -d apps/api/.venv || ! -d apps/web/node_modules || ! -f apps/web/build/index.js ]]; then
  printf 'Run bash scripts/setup.sh first.\n' >&2
  exit 1
fi
stack up -d --wait postgres redis mailpit
# A cloud snapshot can retain files while the Docker service starts with fresh volumes.
if ! stack exec -T postgres sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Atc "SELECT 1 FROM django_migrations LIMIT 1"' >/dev/null 2>&1; then
  (
    cd apps/api
    uv run --frozen python src/manage.py migrate --noinput
    uv run --frozen python "$CAUDAL_ROOT/scripts/seed_demo.py"
  )
fi
exec python3 "$CAUDAL_ROOT/scripts/dev.py"
