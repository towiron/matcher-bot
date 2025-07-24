.PHONY: infra-start infra-stop db-clear refresh-migrations
.SILENT:

# Infrastructure
infra-start: infra-stop
	@docker compose \
		-f docker-compose.yml \
		--env-file .env \
		up --build -d;

infra-stop:
	@docker compose \
		-f docker-compose.yml \
		--env-file .env \
		down > /dev/null 2>&1 || true

db-clear:
	@rm -rf ./temp
	@rm -rf ./database/migrations/versions/*

refresh-migrations:
	@alembic revision --autogenerate -m "Initial migration"
	@alembic upgrade head
