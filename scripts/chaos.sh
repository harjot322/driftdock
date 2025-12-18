#!/bin/sh
set -e

TARGETS="api_v1 api_v2 worker redis postgres"

SERVICE=$(printf "%s\n" $TARGETS | awk 'BEGIN{srand();} {a[NR]=$0} END{print a[int(rand()*NR)+1]}')

echo "Stopping $SERVICE for 15s"
docker compose stop $SERVICE >/dev/null
sleep 15
docker compose start $SERVICE >/dev/null

echo "Recovered $SERVICE"
