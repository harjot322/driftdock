.PHONY: up down logs bootstrap canary chaos backup restore

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=100

bootstrap:
	./scripts/bootstrap.sh

canary:
	./scripts/canary.sh 10

chaos:
	./scripts/chaos.sh

backup:
	./scripts/backup.sh

restore:
	./scripts/restore.sh
