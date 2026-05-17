# Makefile for the SAGA repository.
# Provides convenience targets for development, testing, linting, and documentation.
# Requires GNU make >= 4.0.

.PHONY: all install install-dev lint format typecheck test test-unit test-integration \
        test-property coverage docs docs-serve docker-build docker-push clean help

PYTHON := python
PIP    := pip
PYTEST := pytest
RUFF   := ruff
BLACK  := black
MYPY   := mypy
MKDOCS := mkdocs

SRC_DIR  := src
TEST_DIR := tests
DOCS_DIR := docs

## Default target: run lint, typecheck, and unit tests.
all: lint typecheck test-unit

## Install the package in editable mode with runtime dependencies.
install:
	$(PIP) install -e .

## Install the package in editable mode with all development dependencies.
install-dev:
	$(PIP) install -e ".[dev,docs]"
	pre-commit install

## Run ruff linter and black format-check.
lint:
	$(RUFF) check $(SRC_DIR) $(TEST_DIR)
	$(BLACK) --check $(SRC_DIR) $(TEST_DIR)

## Apply ruff auto-fixes and black formatting.
format:
	$(RUFF) check --fix $(SRC_DIR) $(TEST_DIR)
	$(BLACK) $(SRC_DIR) $(TEST_DIR)

## Run mypy in strict mode.
typecheck:
	$(MYPY) --strict $(SRC_DIR)/saga

## Run all tests (unit + integration + property).
test:
	$(PYTEST) $(TEST_DIR) -q --tb=short

## Run unit tests only (fastest, single CPU, under 5 minutes).
test-unit:
	$(PYTEST) $(TEST_DIR)/unit/ -q --tb=short -m unit

## Run integration tests only.
test-integration:
	$(PYTEST) $(TEST_DIR)/integration/ -q --tb=short -m integration

## Run property-based tests only.
test-property:
	$(PYTEST) $(TEST_DIR)/property/ -q --tb=short -m property

## Run tests with coverage report.
coverage:
	$(PYTEST) $(TEST_DIR) --cov=$(SRC_DIR)/saga --cov-report=html --cov-report=term-missing

## Build the MkDocs Material documentation site.
docs:
	$(MKDOCS) build --strict

## Serve the documentation locally at http://localhost:8000.
docs-serve:
	$(MKDOCS) serve

## Build the Docker image.
docker-build:
	docker build -t olaflaitinen/saga:v1.0.0 -t olaflaitinen/saga:latest .

## Push the Docker image to Docker Hub.
docker-push:
	docker push olaflaitinen/saga:v1.0.0
	docker push olaflaitinen/saga:latest

## Remove Python caches, build artifacts, and test caches.
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf dist/ build/ *.egg-info/ .pytest_cache/ .mypy_cache/ .ruff_cache/ htmlcov/ .coverage site/

## Print available targets.
help:
	@echo "Available targets:"
	@echo "  all            - lint + typecheck + test-unit"
	@echo "  install        - install runtime package"
	@echo "  install-dev    - install dev + docs dependencies, set up pre-commit"
	@echo "  lint           - ruff + black format-check"
	@echo "  format         - apply ruff fixes + black"
	@echo "  typecheck      - mypy strict"
	@echo "  test           - all tests"
	@echo "  test-unit      - unit tests only"
	@echo "  test-integration - integration tests only"
	@echo "  test-property  - property tests only"
	@echo "  coverage       - tests with coverage report"
	@echo "  docs           - build MkDocs site"
	@echo "  docs-serve     - serve docs at localhost:8000"
	@echo "  docker-build   - build Docker image"
	@echo "  docker-push    - push Docker image to Docker Hub"
	@echo "  clean          - remove caches and build artifacts"
