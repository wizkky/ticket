#!/usr/bin/env bash
set -euo pipefail
source "$(dirname -- "$0")/common.sh"
cd "$CAUDAL_ROOT"
command -v uv >/dev/null
command -v corepack >/dev/null
docker info --format '{{.ServerVersion}}' >/dev/null
python3 scripts/configure.py
stack up -d --wait postgres redis mailpit
cd "$CAUDAL_ROOT/apps/api"
uv sync --frozen --group dev
mkdir -p src/staticfiles
uv run --frozen python "$CAUDAL_ROOT/scripts/compile_translations.py"
uv run --frozen python src/manage.py check
uv run --frozen python src/manage.py migrate --noinput
uv run --frozen python src/manage.py collectstatic --noinput
uv run --frozen python "$CAUDAL_ROOT/scripts/seed_demo.py"
cd "$CAUDAL_ROOT/apps/web"
corepack pnpm install --frozen-lockfile
corepack pnpm build
printf 'CaudalTickets demo prepared. Start with bash scripts/dev.sh from the repository root.\n'
