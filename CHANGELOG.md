# Changelog

All notable changes to this project will be documented in this file.

## [1.32.3] - 2026-07-05

### Fixed
- **Critical: restored a runtime that was completely broken.** `__init__.py`
  imported `fontTools.ttLib as ttLib` but referenced `fontTools.ttLib.*`
  throughout, so every font operation raised `NameError: name 'fontTools' is
  not defined` (silently swallowed as "cannot open font"). The tool could not
  process any font. The import is now `import fontTools.ttLib`.
- **`cli.py` failed to import on Python 3.9.** Function signatures used
  `list[str] | None` at definition time without `from __future__ import
  annotations`; the `|` union syntax requires 3.10+. Added the future import so
  the declared `requires-python` floor is actually honored.

### Changed
- Version is now derived from git tags via `hatch-vcs` (`__version__` resolves
  through `importlib.metadata`) instead of a hardcoded string.
- Source distributions no longer bundle the prebuilt GUI installer, codebase
  snapshots, or app-packaging scaffolding: the sdist shrank from ~39 MB to ~31 KB.
- Dropped end-of-life Python 3.8 from the support matrix (now 3.9–3.13);
  `mypy` target updated to 3.10.

### Added
- GitHub Actions: `ci.yml` (ruff + format + mypy + pytest across Python
  3.9–3.13) and `release.yml` (build and publish to PyPI on `v*` tags via
  trusted publishing).

### Internal
- Removed unused imports (`List`, `Optional`, `Set`, the `ttLib` alias) and the
  `warn_unreachable` mypy flag, which produced false positives against the
  `self.success` control-flow pattern. `ruff`, `ruff format`, and `mypy` are
  clean; all 10 tests pass.

## [1.32.2] - 2024-01-XX

### Changed
- **Modernized project tooling and infrastructure** (PR #39):
  - Migrated from Poetry to Hatch build system for better standardization
  - Replaced Black with Ruff for both linting and formatting
  - Added comprehensive Mypy static type checking with type annotations
  - Updated minimum Python version to 3.8+
  - Removed poetry.lock in favor of Hatch's dependency management
  - Fixed escape sequences in pyproject.toml regex patterns

### Improved
- **Enhanced code quality and type safety**:
  - Added type annotations throughout the codebase
  - Fixed type hints in `__init__.py` (SimpleNamespace → Namespace)
  - Improved type precision with Set[int] and List[int] annotations
  - Added mypy configuration with strict optional checking
  - Configured Ruff with comprehensive lint rules (E, F, W, I, UP, B, A, C4, ARG, SIM, PTH, TCH)

### Development
- **Improved developer experience**:
  - Added hatch scripts for common tasks (test, cov, lint, format, typecheck)
  - Enhanced test coverage configuration
  - Modernized Python classifiers to include 3.8-3.12
  - Structured project configuration for better maintainability

### Fixed
- Corrected various type inconsistencies and potential runtime errors
- Enhanced test suite reliability and coverage

## Previous Releases

- [1.32.0] - Previous stable release with core functionality
- Auto-commits for saving local changes
- Various build and deployment improvements