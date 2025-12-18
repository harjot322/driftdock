#!/bin/sh
set -e

STAMP=$(date -u +%Y%m%dT%H%M%SZ)
DEST="./backups/driftdock_${STAMP}.sql"

mkdir -p ./backups

if ! docker compose ps >/dev/null 2>&1; then
  echo "docker compose not running" >&2
  exit 1
fi

docker compose exec -T postgres pg_dump -U drift drift > "$DEST"

echo "Backup written to $DEST"
