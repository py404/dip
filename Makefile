ifneq ($(wildcard .env.local),)
	include .env.local
	export AWS_ACCESS_KEY_ID
	export AWS_SECRET_ACCESS_KEY
	export AWS_DEFAULT_REGION
	export AWS_ENDPOINT_URL
endif

.PHONY: seed-secrets
seed-secrets:
	bash scripts/create-secrets.sh

.PHONY: dev test lint up down logs clean

dev:
	uv run --package dip-api uvicorn dip_api.main:app --reload --port 8000

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run ty check

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +
	rm -rf .venv