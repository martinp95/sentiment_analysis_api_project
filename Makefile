# Makefile for sentiment analysis API project

# Python interpreter
PYTHON = python3

# Directories
APP_DIR = app
TEST_DIR = tests
DOCKER_DIR = docker

COV_OPTIONS = --cov=$(APP_DIR) --cov-report=html --cov-report=term --cov-report=xml

# Default action
.DEFAULT_GOAL := help

# Run unit tests
test: ## Run all test with verbose output
	@echo "Running unit tests..."
	pytest -v

# Run unit tests with coverage
coverage: ## Run test suite with coverage reports (html, xml, terminal)
	@echo "Running unit tests with coverage..."
	pytest -v $(COV_OPTIONS)

# Clean temporary and cache files
clean: ## Clean cache, coverage, pyc files
	@echo "Cleaning project..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -rf htmlcov .pytest_cache .coverage .mypy_cache coverage.xml

# Install dev dependencies
install: ## Install dev requirements
	@echo "Installing development dependencies..."
	pip install -r requirements-dev.txt

# Pre-commit hooks
precommit: ## Run pre-commit hooks on all files
	@echo "Running pre-commit hooks..."
	pre-commit run --all-files

# Docker
up: ## Start Docker containers
	@echo "Starting Docker..."
	cd $(DOCKER_DIR) && docker compose up -d

down: ## Stop Docker containers
	@echo "Stopping Docker..."
	cd $(DOCKER_DIR) && docker compose down

restart: down up ## Restart Docker containers

build: ## Build Docker containers
	@echo "Building Docker containers..."
	cd $(DOCKER_DIR) && docker compose build

# Security checks
security: ## Run static security checks (safety + bandit)
	@echo "Checking security issues..."
	pip install safety bandit
	safety check -r requirements.txt
	bandit -r $(APP_DIR)

# Continuous Integration (full checks)
ci: clean install coverage ## Run full CI check locally

# Help
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'