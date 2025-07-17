# this_file: Makefile

.PHONY: help clean install test lint format typecheck build release test-all dev-setup
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "OpenType Feature Freezer - Available targets:"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "Quick start:"
	@echo "  make dev-setup  # Set up development environment"
	@echo "  make test-all   # Run all tests and checks"
	@echo "  make build      # Build the package"

clean: ## Clean build artifacts and caches
	@echo "🧹 Cleaning build artifacts..."
	rm -rf dist/ build/ src/opentype_feature_freezer/_version.py
	rm -rf .coverage htmlcov/ .pytest_cache/ .mypy_cache/ .ruff_cache/
	rm -rf src/opentype_feature_freezer.egg-info/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	@echo "✅ Clean completed"

dev-setup: ## Set up development environment
	@echo "🔧 Setting up development environment..."
	python -m pip install --upgrade pip
	python -m pip install hatch
	python -m pip install -e .[dev]
	@echo "✅ Development environment ready"

install: ## Install package in development mode
	@echo "📦 Installing package in development mode..."
	python -m pip install -e .
	@echo "✅ Package installed"

test: ## Run tests
	@echo "🧪 Running tests..."
	hatch run test

test-cov: ## Run tests with coverage
	@echo "🧪 Running tests with coverage..."
	hatch run cov

test-all: ## Run all tests and checks (lint, format, typecheck, coverage)
	@echo "🚀 Running all tests and checks..."
	hatch run test-all

lint: ## Run linting
	@echo "🔍 Running linting..."
	hatch run lint

lint-fix: ## Run linting with auto-fix
	@echo "🔧 Running linting with auto-fix..."
	hatch run lint-fix

format: ## Format code
	@echo "✨ Formatting code..."
	hatch run format

format-check: ## Check code formatting
	@echo "🔍 Checking code formatting..."
	hatch run format-check

typecheck: ## Run type checking
	@echo "🔍 Running type checking..."
	hatch run typecheck

build: clean ## Build the package
	@echo "🏗️  Building package..."
	hatch build
	@echo "✅ Build completed"
	@echo "📦 Distribution files:"
	@ls -la dist/

build-gui: ## Build GUI executables (platform-specific)
	@echo "🖥️  Building GUI executables..."
	@if [ "$$(uname)" = "Darwin" ]; then \
		cd app && pyinstaller --clean pyinstaller-mac.spec; \
	elif [ "$$(expr substr $$(uname -s) 1 5)" = "Linux" ]; then \
		echo "GUI build not supported on Linux"; \
	elif [ "$$(expr substr $$(uname -s) 1 10)" = "MINGW32_NT" ] || [ "$$(expr substr $$(uname -s) 1 10)" = "MINGW64_NT" ]; then \
		cd app && pyinstaller --clean pyinstaller-win.spec; \
	else \
		echo "Unknown platform: $$(uname)"; \
	fi

release: ## Create a release (run tests, build, and tag)
	@echo "🚀 Creating release..."
	@if [ -z "$(VERSION)" ]; then \
		echo "❌ Please specify VERSION: make release VERSION=1.33.0"; \
		exit 1; \
	fi
	@./scripts/release.sh $(VERSION)

check-deps: ## Check for security vulnerabilities in dependencies
	@echo "🔒 Checking for security vulnerabilities..."
	python -m pip install safety
	safety check

benchmark: ## Run performance benchmarks
	@echo "⚡ Running benchmarks..."
	@if [ -f "benchmarks/run_benchmarks.py" ]; then \
		python benchmarks/run_benchmarks.py; \
	else \
		echo "No benchmarks found"; \
	fi

docs: ## Build documentation
	@echo "📚 Building documentation..."
	@if [ -f "docs/Makefile" ]; then \
		cd docs && make html; \
	else \
		echo "No documentation setup found"; \
	fi

# Development workflow targets
dev-test: ## Quick development test (no coverage)
	@echo "🏃 Running quick tests..."
	python -m pytest tests/ -v --tb=short

dev-install: ## Install in development mode with all dependencies
	@echo "🔧 Installing for development..."
	python -m pip install -e .[dev,gui]

# CI/CD helpers
ci-test: ## Run tests in CI environment
	@echo "🤖 Running CI tests..."
	python -m pytest tests/ -v --cov=src/opentype_feature_freezer --cov-report=xml --cov-report=term-missing

ci-build: ## Build in CI environment
	@echo "🤖 Building in CI..."
	python -m build

# Platform-specific targets
mac-build: ## Build for macOS
	@echo "🍎 Building for macOS..."
	make build
	make build-gui

win-build: ## Build for Windows
	@echo "🪟 Building for Windows..."
	make build
	make build-gui

linux-build: ## Build for Linux
	@echo "🐧 Building for Linux..."
	make build