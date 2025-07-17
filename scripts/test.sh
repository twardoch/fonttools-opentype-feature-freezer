#!/bin/bash
# this_file: scripts/test.sh

set -e

echo "🧪 Testing OpenType Feature Freezer..."

# Install test dependencies
echo "📦 Installing test dependencies..."
python -m pip install --upgrade pip
python -m pip install -e .[dev]

# Run linting
echo "🔍 Running linting..."
python -m ruff check src tests

# Run type checking
echo "🔍 Running type checking..."
python -m mypy src tests

# Run tests with coverage
echo "🧪 Running tests with coverage..."
python -m pytest tests/ -v --cov=src/opentype_feature_freezer --cov-report=term-missing --cov-report=html

# Check if coverage meets minimum threshold
echo "📊 Checking coverage threshold..."
python -m coverage report --fail-under=80

echo "✅ All tests passed!"