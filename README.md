# DriftDock

A local-first DevOps lab that simulates real release engineering: blue/green + canary routing, queue-based workloads, chaos drills, and point-in-time backups. No cloud required. Optional AWS free-tier Terraform is included but never needed to run locally.

## What makes this different
- Canary routing with live traffic controls (Nginx split + header overrides)
- Background worker pipeline with Redis + Postgres state transitions
- Chaos drills that kill and recover critical services
- Backup/restore flows that are auditable and reproducible
- Everything runs locally via Docker Compose

## Quick start
1. `docker compose up -d --build`
2. `./scripts/bootstrap.sh`
3. Send traffic:
   - `curl -s http://localhost:8080/health | jq`
   - `curl -s -X POST http://localhost:8080/events -H 'Content-Type: application/json' -d '{"type":"signup","payload":{"user":"ada"}}' | jq`
4. Watch status:
   - `curl -s http://localhost:8080/stats | jq`
5. Optional load profile:
   - `docker compose --profile load up -d`

## Canary controls
- Set canary to 10%: `./scripts/canary.sh 10`
- Force a request to canary: `curl -H 'X-Canary: always' http://localhost:8080/health`
- Force stable: `curl -H 'X-Canary: never' http://localhost:8080/health`

## Chaos drills
- Kill a random critical service for 15s: `./scripts/chaos.sh`

## Backups
- Create a backup: `./scripts/backup.sh`
- Restore from latest: `./scripts/restore.sh`

## Optional AWS free-tier (not required)
`infra/aws-free-tier` includes a minimal S3 bucket + IAM policy for storing backups. It is isolated and not used by default.

## Architecture
- `gateway` (Nginx) routes traffic to `api_v1` and `api_v2` using canary percentage
- `api_*` writes events to Postgres and enqueues jobs in Redis
- `worker` processes jobs and updates event status
- `minio` provides local object storage (optional)

## Ports
- 8080: gateway
- 5432: postgres
- 6379: redis
- 9000/9001: minio

## Project layout
- `api/` Flask API service
- `worker/` background worker
- `nginx/` canary router
- `scripts/` operational tooling
- `infra/aws-free-tier/` optional Terraform
