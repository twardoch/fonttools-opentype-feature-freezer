# Refactoring Plan: Splitting Large Code Files

This plan outlines how to refactor the largest code files in the `fonttools-opentype-feature-freezer` project into smaller, more manageable units while maintaining existing functionality.

## 1. Refactoring `src/opentype_feature_freezer/__init__.py`

This file currently contains the monolithic `RemapByOTL` class, which handles various aspects of font processing. The goal is to break down this class into smaller, more focused modules/classes, adhering to the Single Responsibility Principle.

**Current State:**
The `RemapByOTL` class is responsible for:
- Font I/O (opening, saving, closing)
- Initializing glyph substitutions
- Filtering OpenType features and lookups
- Applying glyph substitutions
- Remapping CMAP tables
- Renaming font metadata
- Reporting font information

**Proposed Structure:**

```
src/opentype_feature_freezer/
├── __init__.py             # Orchestrates the new modules/classes
├── font_io.py              # Handles font opening, saving, and closing
├── feature_processing.py   # Handles feature/lookup filtering and substitution application
├── cmap_remapping.py       # Handles CMAP table remapping
├── font_naming.py          # Handles font renaming logic
├── reporting.py            # Handles font information reporting
└── exceptions.py           # Custom exceptions (as per PLAN.md)
```

**Detailed Plan:**

1.  **Create `src/opentype_feature_freezer/font_io.py`:**
    *   Move `_openFontTTX`, `openFont`, `_saveFontTTX`, `saveFont`, `_closeFontTTX`, `closeFont` methods into a new class, e.g., `FontIOHandler`.
    *   The `FontIOHandler` class will take the `ttLib.TTFont` object as an argument in its methods or be initialized with it.
    *   Update `RemapByOTL` to instantiate and use `FontIOHandler` for font I/O operations.

2.  **Create `src/opentype_feature_freezer/feature_processing.py`:**
    *   Move `initSubs`, `filterFeatureIndex`, `filterLookupList`, and `applySubstitutions` methods into a new class, e.g., `FeatureProcessor`.
    *   This class will be initialized with the `ttLib.TTFont` object and the `options` (or relevant parts of it).
    *   It will manage `subs0`, `subs1`, `FeatureIndex`, `filterByFeatures`, `filterByLangSys`, `filterByScript`, `LookupList`, and `substitution_mapping`.
    *   Update `RemapByOTL` to instantiate and use `FeatureProcessor`.

3.  **Create `src/opentype_feature_freezer/cmap_remapping.py`:**
    *   Move `remapCmaps` method into a new class, e.g., `CmapRemapper`.
    *   This class will take the `ttLib.TTFont` object and the `substitution_mapping` as arguments.
    *   Update `RemapByOTL` to instantiate and use `CmapRemapper`.

4.  **Create `src/opentype_feature_freezer/font_naming.py`:**
    *   Move `renameFont` method into a new class, e.g., `FontNamer`.
    *   This class will take the `ttLib.TTFont` object, `options`, and `filterByFeatures` (for suffix generation) as arguments.
    *   Update `RemapByOTL` to instantiate and use `FontNamer`.

5.  **Create `src/opentype_feature_freezer/reporting.py`:**
    *   Move `_reportFont` method into a new class, e.g., `Reporter`.
    *   This class will take `reportLangSys` and `reportFeature` as arguments.
    *   Update `RemapByOTL` to instantiate and use `Reporter`.

6.  **Update `src/opentype_feature_freezer/__init__.py`:**
    *   The `RemapByOTL` class will become a coordinator. Its `__init__` will initialize instances of the new classes.
    *   The `run` method will orchestrate the calls to methods in these new instances.
    *   Ensure proper passing of `ttLib.TTFont` object and `options` (or specific attributes from `options`) to the new classes.
    *   Adjust imports to reflect the new module structure.

7.  **Refactor `RemapByOTL.run()`:**
    *   The `run` method should be simplified to a sequence of calls to the new, specialized objects.
    *   Consider using a `try...finally` block for `closeFont` to ensure the font is always closed.

8.  **Update `src/opentype_feature_freezer/cli.py` and `app/OTFeatureFreezer.py`:**
    *   Adjust imports if `RemapByOTL`'s location or name changes, or if any other directly imported components are moved.
    *   Ensure the `options` object (Namespace) passed to `RemapByOTL` remains compatible with its new `__init__` signature.

9.  **Update Tests:**
    *   Modify existing tests in `tests/test_freeze.py` and `tests/test_rename.py` to reflect the new class structure. This will likely involve mocking or directly instantiating the new, smaller classes for unit testing, and ensuring integration tests still work with the refactored `RemapByOTL`.

## 2. Refactoring `tests/test_rename.py`

This test file can be split based on the type of font being tested (TTF vs. OTF) to improve organization and readability.

**Current State:**
`tests/test_rename.py` contains tests for both TTF and OTF font renaming.

**Proposed Structure:**

```
tests/
├── test_freeze.py
├── test_rename_ttf.py  # New file for TTF renaming tests
├── test_rename_otf.py  # New file for OTF renaming tests
└── conftest.py
```

**Detailed Plan:**

1.  **Create `tests/test_rename_ttf.py`:**
    *   Move `test_rename_ttf`, `test_rename_ttf_no_replace`, `test_rename_ttf_autosuffix`, and `test_rename_ttf_with_nameid16` from `tests/test_rename.py` to `tests/test_rename_ttf.py`.
    *   Ensure all necessary imports (`fontTools.ttLib`, `opentype_feature_freezer`, `Namespace`, `shared_datadir`) are present in the new file.

2.  **Create `tests/test_rename_otf.py`:**
    *   Move `test_rename_otf` and `test_rename_otf_with_nameid16` from `tests/test_rename.py` to `tests/test_rename_otf.py`.
    *   Ensure all necessary imports are present in the new file.

3.  **Delete `tests/test_rename.py`:**
    *   Once all tests are moved, delete the original `tests/test_rename.py` file.

## 3. Refactoring `app/dmgbuild_settings.py`

This file contains utility functions that are not directly related to DMG build settings and can be extracted into a more general utility module.

**Current State:**
`app/dmgbuild_settings.py` contains `get_version` and `icon_from_app` functions.

**Proposed Structure:**

```
app/
├── dmgbuild_settings.py    # Main settings file
├── utils.py                # General utility functions (e.g., get_version)
├── mac_app_utils.py        # macOS-specific utility functions (e.g., icon_from_app)
└── ...
```

**Detailed Plan:**

1.  **Create `app/utils.py`:**
    *   Move the `get_version` function from `app/dmgbuild_settings.py` to `app/utils.py`.
    *   Update the import path for `__init__.py` within `get_version` if necessary (it currently uses `../src/opentype_feature_freezer/__init__.py`, which might need adjustment if `utils.py` is moved to a different level).

2.  **Create `app/mac_app_utils.py`:**
    *   Move the `icon_from_app` function from `app/dmgbuild_settings.py` to `app/mac_app_utils.py`.
    *   Ensure `biplist` is imported in `mac_app_utils.py`.

3.  **Update `app/dmgbuild_settings.py`:**
    *   Import `get_version` from `app.utils`.
    *   Import `icon_from_app` from `app.mac_app_utils`.
    *   Remove the original definitions of these functions.

4.  **Update `app/macdeploy`:**
    *   If `get_version` is used directly in `macdeploy` (which it is), ensure the `perl` command still correctly locates `__init__.py` or update it to call the new `get_version` function from `app.utils`. For simplicity, it might be best to leave the `perl` command as is, as it's a shell script and not Python.

**General Considerations for all Refactorings:**

*   **Imports:** Pay close attention to import statements. When moving code, ensure that all necessary modules are correctly imported in their new locations and that old references are updated.
*   **Relative vs. Absolute Imports:** Prefer absolute imports (e.g., `from opentype_feature_freezer.font_io import FontIOHandler`) within the package to avoid issues with how Python resolves relative imports.
*   **Type Hinting:** Maintain and update existing type hints, and add new ones where appropriate, especially for new function signatures or class attributes.
*   **Testing:** After each refactoring step, run the relevant tests (and ideally all tests) to ensure no regressions have been introduced.
*   **Version Control:** Perform these changes in small, atomic commits. Each commit should ideally represent a single logical refactoring step.
*   **Docstrings and Comments:** Update docstrings and comments to reflect the new structure and responsibilities of classes and functions.
*   **`pyproject.toml` and `mypy.ini`:** Ensure that the `source` paths in `pyproject.toml` for coverage and `mypy` configuration in `mypy.ini` are updated to include the new files/directories.
*   **`PLAN.md` and `TODO.md`:** Update these files to reflect the completed refactoring tasks and any new tasks that arise from the refactoring.
