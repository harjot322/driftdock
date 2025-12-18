#!/bin/sh
set -e

export CANARY_PERCENT=${CANARY_PERCENT:-10}

envsubst '${CANARY_PERCENT}' < /etc/nginx/templates/canary.conf.template > /etc/nginx/conf.d/default.conf

exec "$@"
