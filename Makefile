.PHONY: infra-start infra-stop db-clear refresh-migrations local
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

local:
	@python database/seed/seed.py
	@python bot-runner.py

generate-users:
	@count=$(or $(count), 1); \
	echo "👥 Генерация $$count пользователей..."; \
	python database/seed/fake_users.py --count=$$count