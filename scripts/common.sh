#!/usr/bin/env bash
set -euo pipefail
CAUDAL_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
export UV_CACHE_DIR="${UV_CACHE_DIR:-$CAUDAL_ROOT/.local/cache/uv}"
export UV_PYTHON_INSTALL_DIR="${UV_PYTHON_INSTALL_DIR:-$CAUDAL_ROOT/.local/python}"
export COREPACK_HOME="${COREPACK_HOME:-$CAUDAL_ROOT/.local/corepack}"
export NODE_USE_ENV_PROXY="${NODE_USE_ENV_PROXY:-1}"
export npm_config_store_dir="${npm_config_store_dir:-$CAUDAL_ROOT/.local/pnpm-store}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$CAUDAL_ROOT/.local/cache}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$CAUDAL_ROOT/.local/share}"
export NO_PROXY="${NO_PROXY:+$NO_PROXY,}localhost,127.0.0.1,::1"
export no_proxy="$NO_PROXY"
export COMPOSE_PROGRESS="${COMPOSE_PROGRESS:-plain}"
mkdir -p "$CAUDAL_ROOT/.local"

stack() {
  docker compose --project-directory "$CAUDAL_ROOT" --env-file "$CAUDAL_ROOT/.local/stack.env" "$@"
}
