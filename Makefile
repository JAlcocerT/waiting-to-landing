# Project Documentation Generator Makefile
# This Makefile automates Docker setup and script execution

# Default make goal
.DEFAULT_GOAL := help

# Load environment variables from .env file
include .env
export

.PHONY: help run build clean check-env show-logs

.PHONY: help
help: ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

# Check for environment file
check-env: ## Check if .env file exists with OpenAI API key for Codex
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Please create it with your OpenAI API key for Codex."; \
		exit 1; \
	fi
	@echo ".env file found"

local-dev:
	@echo "Running Astro development server..."
	npm install && npm run dev -- --host 0.0.0.0
	@echo "Astro development server running"

local-prod:
	@echo "Running Astro production server..."
	npm install && npm run build && npm run start
	@echo "Astro production server running"

# Build all containers
build: check-env
	@echo "Building all Docker containers..."
	docker compose -f docker-compose.yml build
	@echo "Docker containers built successfully"

run-all:	## Build and Spin the 3 containers (Codex, Astro dev, Astro prod)
	@echo "Running all services (Codex, Astro dev, Astro prod)..."
	docker compose -f docker-compose.yml up --build astro-dev astro-prod codex

run-dev:	## Run only the astro development server to see the docs generated in real time
	@echo "Running Astro development server..."
	docker compose -f docker-compose.yml up --build astro-dev codex

run-prod:	## Run only the astro production server with the generated docs and search capability
	@echo "Running Astro production server..."
	docker compose -f docker-compose.yml up --build astro-prod codex

# Show logs for running containers
show-logs:
	@echo "Showing logs for running containers..."
	docker compose -f docker-compose.yml logs -f

# Clean up containers and images
clean:
	@echo "Cleaning up Docker containers and images..."
	docker compose -f docker-compose.yml down
	docker compose -f docker-compose.yml rm -f
	@echo "Cleanup completed"

build-codex:	## Build Codex container only
	@echo "Building Codex container specifically..."
	docker compose -f docker-compose.codex.yml build
	@echo "Codex container built successfully"

run-codex-only:	## Run only the Codex container (codex-container) via codex compose file and keeps it running
	@echo "Running only the Codex container from codex compose file..."
	docker compose -f docker-compose.codex.yml up codex

codex-shell:	## Open an interactive shell in the codex container so that the scripts are run without local dependencies
	@echo "Running Codex container...the scripts run_codex-init.sh and run_codex-followup.sh are available to run without any local dependencies"
	docker exec -it codex-container bash