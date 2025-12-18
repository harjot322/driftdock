#!/bin/sh
set -e

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is required" >&2
  exit 1
fi

echo "Waiting for services..."
for i in $(seq 1 20); do
  if docker compose ps >/dev/null 2>&1; then
    if docker compose exec -T postgres pg_isready -U drift >/dev/null 2>&1; then
      echo "Postgres ready"
      break
    fi
  fi
  sleep 1
  if [ "$i" -eq 20 ]; then
    echo "Postgres not ready" >&2
    exit 1
  fi
done

echo "Seeding initial events"
for i in $(seq 1 5); do
  curl -s -X POST http://localhost:8080/events \
    -H 'Content-Type: application/json' \
    -d "{\"type\":\"seed\",\"payload\":{\"index\":$i}}" >/dev/null
  sleep 0.2
done

echo "Done"
