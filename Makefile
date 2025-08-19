.PHONY: infra-start infra-stop db-clear refresh-migrations local
.SILENT:

# Infrastructure
infra-start: infra-stop
	@docker compose \
		-f docker-compose.dev.yml \
		--env-file .env.dev \
		up --build -d;

infra-stop:
	@docker compose \
		-f docker-compose.dev.yml \
		--env-file .env.dev \
		down > /dev/null 2>&1 || true

db-clear:
	@rm -rf ./temp

refresh-migrations:
# 	@alembic revision --autogenerate
	@alembic upgrade head

local:
	@python database/seed/seed.py
	@python bot-runner.py

generate-users:
	@count=$(or $(count), 1); \
	echo "👥 Генерация $$count пользователей..."; \
	python database/seed/fake_users.py --count=$$count