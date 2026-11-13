.PHONY: help rundev build up log fast lf lint format

help: ## Show this help
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

rundev: ## Run Django development server
	uv run page collectstatic --no-input && uv run runserver

build: ## Just make docker build
	docker compose build

up: ## Start docker build
	docker compose up -d

log: ## Show logs of running build
	docker compose logs -f

fast: ## Fast project setup, build & up
	docker compose build && docker compose up

lf: ## Lint and format (ruff + mypy)
	uv run ruff format .
	uv run ruff check . --fix
	uv run mypy .

lint: ## Type-check with mypy
	uv run mypy .

format: ## Format and autofix with ruff
	uv run ruff format .
	uv run ruff check . --fix
