# Release Guide

This guide explains how to use the git-tag-based semversioning and CI/CD system implemented for the OpenType Feature Freezer project.

## Overview

The project now has a complete automated release pipeline that:
- Uses git tags for semantic versioning
- Automatically builds multiplatform binaries
- Runs comprehensive tests
- Publishes to PyPI
- Creates GitHub releases

## Quick Start

### 1. Development Workflow

```bash
# Set up development environment
make dev-setup

# Run tests during development
make test

# Run all checks (lint, format, typecheck, coverage)
make test-all

# Build the package
make build
```

### 2. Creating a Release

```bash
# Create a new release (replace 1.33.0 with your version)
make release VERSION=1.33.0
```

This will:
- Run all tests
- Update CHANGELOG.md
- Create and push a git tag
- Trigger automated CI/CD pipeline

### 3. Local Scripts

Three main scripts are available:

```bash
# Build packages and executables
./scripts/build.sh

# Run comprehensive tests
./scripts/test.sh

# Create a release (interactive)
./scripts/release.sh 1.33.0
```

## Versioning System

### Git Tag Based Versioning

The project uses `hatch-vcs` for automatic version management:

- **Development versions**: `1.0.1.dev0+ge23a1f6.d20250717`
- **Released versions**: `1.33.0` (from git tag `v1.33.0`)

### Version Sources

1. **Git tags**: `v1.33.0` → `1.33.0`
2. **Development**: Automatic dev versions based on commits since last tag
3. **Fallback**: `0.0.0+unknown` if no git or tags

### Creating Version Tags

```bash
# Create and push a new version tag
git tag -a v1.33.0 -m "Release v1.33.0"
git push origin v1.33.0
```

## CI/CD Pipeline

> **⚠️ IMPORTANT**: Before using the CI/CD pipeline, you must activate the GitHub Actions workflows. See `WORKFLOW_SETUP.md` for instructions.

### GitHub Actions Workflows

#### 1. CI Workflow (`.github/workflows/ci.yml`)

**Triggers**: Push to master, Pull requests

**Jobs**:
- **Test**: Runs on Python 3.8-3.12, Ubuntu/Windows/macOS
- **Build**: Creates Python packages (wheels and sdist)
- **Build GUI**: Creates GUI executables for Windows and macOS

**What it does**:
- Linting with Ruff
- Type checking with MyPy
- Tests with pytest
- Coverage reporting
- Multiplatform compatibility testing

#### 2. Release Workflow (`.github/workflows/release.yml`)

**Triggers**: Git tags (`v*`)

**Jobs**:
- **Test**: Validates the release
- **Build Python**: Creates PyPI packages
- **Build GUI**: Creates platform-specific executables
- **Release**: Creates GitHub release with assets
- **Publish PyPI**: Uploads to PyPI automatically

**Artifacts produced**:
- Python wheel and source distribution
- Windows GUI executable (zip)
- macOS GUI executable (zip)
- Automatic GitHub release
- PyPI package

### Setting Up Secrets

For the CI/CD pipeline to work fully, configure these GitHub secrets:

```
PYPI_API_TOKEN    # PyPI API token for publishing
CODECOV_TOKEN     # Optional: Codecov token for coverage reporting
```

## Testing

### Test Structure

```
tests/
├── conftest.py           # Test configuration
├── test_cli.py          # CLI interface tests
├── test_core.py         # Core functionality tests
├── test_freeze.py       # Font freezing tests
├── test_rename.py       # Font renaming tests
└── test_version.py      # Version system tests
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
hatch run test tests/test_version.py

# Run tests with specific markers
hatch run test -m "not slow"
```

### Test Coverage

The project aims for >80% test coverage. Coverage reports are generated in:
- Terminal output
- HTML report in `htmlcov/`
- XML report for CI systems

## Building

### Local Building

```bash
# Build Python packages
make build

# Build GUI executables (macOS/Windows only)
make build-gui

# Clean build artifacts
make clean
```

### Build Artifacts

**Python packages**:
- `dist/*.whl` - Wheel distribution
- `dist/*.tar.gz` - Source distribution

**GUI executables**:
- `app/dist/OTFeatureFreezer.app` (macOS)
- `app/dist/OTFeatureFreezer.exe` (Windows)

## Project Structure

```
├── .github/workflows/    # GitHub Actions CI/CD
├── app/                  # GUI application files
├── scripts/              # Build and release scripts
├── src/                  # Source code
├── tests/                # Test suite
├── Makefile             # Convenient build targets
├── pyproject.toml       # Project configuration
├── pytest.ini          # Test configuration
└── RELEASE_GUIDE.md     # This file
```

## Configuration Files

### `pyproject.toml`

Key configurations:
- **Build system**: Hatch with hatch-vcs
- **Dependencies**: Runtime and development
- **Scripts**: Hatch environment scripts
- **Tools**: Ruff, MyPy, Coverage settings

### `pytest.ini`

Test configuration:
- Test paths and Python paths
- Test markers
- Warning filters
- Output formatting

### GitHub Actions

- **Matrix testing**: Multiple Python versions and platforms
- **Artifact handling**: Automated asset creation
- **Release automation**: GitHub releases and PyPI publishing

## Troubleshooting

### Common Issues

1. **Version not detected**: Ensure git tags are pushed
2. **Build failures**: Check Python version compatibility
3. **Test failures**: Run tests locally first
4. **GUI build issues**: Platform-specific dependencies required

### Debug Commands

```bash
# Check version detection
python -c "import opentype_feature_freezer; print(opentype_feature_freezer.__version__)"

# Test CLI tool
pyftfeatfreeze --version

# Check git tags
git tag -l

# Verify build environment
hatch env show
```

## Release Checklist

Before creating a release:

- [ ] All tests passing locally
- [ ] CHANGELOG.md updated
- [ ] Version number decided
- [ ] No uncommitted changes
- [ ] On master branch
- [ ] CI passing on latest commit

After creating a release:

- [ ] Verify GitHub release created
- [ ] Check PyPI package published
- [ ] Test installation from PyPI
- [ ] Verify GUI executables work
- [ ] Update documentation if needed

## Future Enhancements

Potential improvements to the release system:

1. **Automated changelog**: Generate from commit messages
2. **Pre-release versions**: Support alpha/beta/rc versions
3. **Docker images**: Automated Docker Hub publishing
4. **Package managers**: Homebrew, Chocolatey, etc.
5. **Security scanning**: Automated vulnerability checks
6. **Performance benchmarks**: Automated performance tracking

---

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>