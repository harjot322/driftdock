#!/bin/sh
set -e

SRC=$1

if [ -z "$SRC" ]; then
  SRC=$(ls -t ./backups/*.sql 2>/dev/null | head -n 1 || true)
fi

if [ -z "$SRC" ]; then
  echo "no backup found" >&2
  exit 1
fi

if [ ! -f "$SRC" ]; then
  echo "backup not found: $SRC" >&2
  exit 1
fi

docker compose exec -T postgres psql -U drift -d drift -c "DROP TABLE IF EXISTS events CASCADE;"
docker compose exec -T postgres psql -U drift -d drift < "$SRC"

echo "Restored from $SRC"
