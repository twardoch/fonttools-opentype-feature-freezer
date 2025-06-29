# Changelog

All notable changes to this project will be documented in this file.

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