#!/bin/sh
set -eu
# SQLite needs /data; PostgreSQL keeps all state in the remote database.
if [ -z "${DATABASE_URL:-}" ]; then
  case "${DATABASE_PATH:-/data/alerta.db}" in
    /data/*) ;;
    *) echo "Container DATABASE_PATH must be inside /data." >&2; exit 1 ;;
  esac
  mkdir -p /data
fi
if [ "$(id -u)" = "0" ]; then
  if [ -z "${DATABASE_URL:-}" ]; then
    chown -R appuser:appuser /data
  fi
  exec gosu appuser "$@"
fi
exec "$@"
