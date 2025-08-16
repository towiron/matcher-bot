.PHONY: infra-start infra-stop db-clear refresh-migrations migrate-upgrade setup local api
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

migrate-upgrade:
	@poetry run alembic upgrade head

refresh-migrations:
	@poetry run alembic upgrade head
	@poetry run alembic revision --autogenerate -m "Initial migration"
	@poetry run alembic upgrade head

setup:
	@make infra-start
	@sleep 5
	@make refresh-migrations
	@poetry run python bot/database/seed/seed.py

local:
	@poetry run python bot/database/seed/seed.py
	@poetry run python bot/bot_runner.py

api:
	@poetry run python api/service_runner.py

generate-users:
	@count=$(or $(count), 1); \
	echo "👥 Генерация $$count пользователей..."; \
	poetry run python bot/database/seed/fake_users.py --count=$$count