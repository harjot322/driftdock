#!/bin/sh
set -e

if [ -z "$1" ]; then
  echo "usage: ./scripts/canary.sh <percent>" >&2
  exit 1
fi

PERCENT=$1

if ! echo "$PERCENT" | grep -E '^[0-9]+$' >/dev/null 2>&1; then
  echo "percent must be an integer" >&2
  exit 1
fi

if [ "$PERCENT" -lt 0 ] || [ "$PERCENT" -gt 100 ]; then
  echo "percent must be 0-100" >&2
  exit 1
fi

docker compose exec -T gateway sh -c "sed -i \"s/[0-9]\\+%/${PERCENT}%/\" /etc/nginx/conf.d/default.conf && nginx -s reload"

echo "Canary set to ${PERCENT}%"
