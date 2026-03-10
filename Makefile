.DEFAULT_GOAL := help

# ── Help ──────────────────────────────────────────────────────────────────────

.PHONY: help
help: ## Show this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} \
		/^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } \
		/^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)

# ── Docker ────────────────────────────────────────────────────────────────────

##@ Docker

.PHONY: build
build: ## Build images and start containers
	docker compose up --build

.PHONY: restart
restart: ## Restart containers (no rebuild)
	docker compose restart

.PHONY: up
up: ## Start containers (no rebuild)
	docker compose up

.PHONY: upd
upd: ## Start containers in detached mode (no rebuild)
	docker compose up -d

.PHONY: down
down: ## Stop and remove containers
	docker compose down

.PHONY: logs
logs: ## Tail container logs
	docker compose logs --follow

.PHONY: shell
shell: ## Open a bash shell inside the running app container
	docker compose exec app bash

# ── Code quality ──────────────────────────────────────────────────────────────

##@ Code quality

.PHONY: format
format: ## Auto-format code with ruff (format + lint --fix)
	docker compose exec app /bin/bash /app/scripts/format.sh

.PHONY: code-checks
code-checks: ## Run all static checks (ruff format, ruff lint, mypy, bandit)
	docker compose exec app /bin/bash /app/scripts/code-checks.sh

.PHONY: run-tests
run-tests: ## Run the test suite with coverage
	docker compose exec app /bin/bash /app/scripts/run-tests.sh
