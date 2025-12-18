# DriftDock Runbook

## Incident drill: queue backlog
1. Check backlog: `redis-cli -h localhost llen driftdock:events`
2. Verify workers are healthy: `docker compose ps worker`
3. If worker down, restart: `docker compose restart worker`
4. Watch statuses: `curl -s http://localhost:8080/stats | jq`

## Incident drill: canary regression
1. Reduce canary to 0%: `./scripts/canary.sh 0`
2. Validate stable: `curl -s http://localhost:8080/health | jq`
3. Collect error sample: `docker compose logs api_v2 --tail=50`
4. If resolved, reintroduce: `./scripts/canary.sh 5`

## Recovery drill: restore data
1. Snapshot: `./scripts/backup.sh`
2. Restore: `./scripts/restore.sh`
3. Verify: `curl -s http://localhost:8080/stats | jq`
