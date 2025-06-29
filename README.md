# OpenType Feature Freezer: Make Advanced Typography Accessible Everywhere

**OpenType Feature Freezer** is a powerful tool designed to make sophisticated typographic features, like small caps or old-style numerals, accessible by default in your fonts. This means you can use these features even in applications with limited or no OpenType support.

## Part 1: For Everyone Using Fonts

### What Does It Do?

Many professional fonts come with "OpenType features" – special typographic effects such as true small capitals, alternative character shapes, ligatures, or figures (numbers) that align differently with text. Normally, you need specific software that allows you to turn these features on.

OpenType Feature Freezer modifies a font file so that selected OpenType features are "frozen" into it. The characters that were previously only accessible via these features become the default characters in the modified font.

For example, if you freeze the "small caps" (`smcp`) feature, typing lowercase letters will directly produce small capitals.

### Who Is It For?

This tool is for anyone who wants to use advanced typographic features in applications that don't provide easy access to OpenType controls. This includes:

*   Users of office suites like LibreOffice or OpenOffice.
*   Graphic designers working with software that might not support specific OpenType features (e.g., some versions of Microsoft Office have limited small caps support).
*   Anyone who wants a font variant where certain features are always active without manual intervention.

### Why Is It Useful?

*   **Accessibility:** Unlocks advanced typography in a wider range of applications.
*   **Consistency:** Ensures that specific typographic styles (like old-style figures) are used consistently without needing to remember to enable features.
*   **Convenience:** Creates ready-to-use font versions with desired features baked in.

### Installation

OpenType Feature Freezer is available in two forms:

*   **OTFeatureFreezer (GUI):** A graphical application for macOS and Windows.
*   **pyftfeatfreeze (CLI):** A command-line tool for users comfortable with terminal commands.

#### OTFeatureFreezer GUI App (macOS)

1.  **[Download the DMG for macOS](https://github.com/twardoch/fonttools-opentype-feature-freezer/raw/master/download/OTFeatureFreezer.dmg)**
2.  Open the downloaded DMG file.
3.  Drag the `OTFeatureFreezer.app` icon to your `/Applications` folder.
4.  **First Run:** Ctrl+click the `OTFeatureFreezer.app` icon in `/Applications`, choose "Open" from the menu, and then click "Open" in the dialog box.
5.  Subsequent Runs: Double-click the app icon.

#### OTFeatureFreezer GUI App (Windows 64-bit)

1.  **[Download the ZIP for Windows](https://github.com/twardoch/fonttools-opentype-feature-freezer/raw/master/download/OTFeatureFreezer.zip)**
2.  You need a 64-bit version of Windows (7 or newer).
3.  Unzip the downloaded file.
4.  Run `setup_featfreeze.exe` to install the application.
5.  Launch "OTFeatureFreezer" from your Start Menu.

#### pyftfeatfreeze CLI App (All Platforms)

This requires Python 3.6 or newer. If you don't have Python, get it from [python.org](https://www.python.org/) or your system's package manager.

**Recommended Method (using pipx):**
Pipx installs Python command-line tools in isolated environments, which is clean and convenient.
```bash
pipx install opentype-feature-freezer
```
To upgrade later:
```bash
pipx upgrade opentype-feature-freezer
```

**Alternative Method (using pip):**
It's generally recommended to run `pip` via `python3 -m pip` to ensure you're using `pip` associated with the correct Python installation, especially if you have multiple Python versions.
It's best to do this inside a Python virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python3 -m pip install --upgrade opentype-feature-freezer
```
If the above fails, or for a user-specific installation (avoids needing admin rights):
```bash
python3 -m pip install --user --upgrade opentype-feature-freezer
```

**Development Version (from GitHub - for testing latest changes):**
```bash
python3 -m pip install --upgrade git+https://github.com/twardoch/fonttools-opentype-feature-freezer
```

### How to Use

#### Using the OTFeatureFreezer GUI

The GUI provides an easy-to-use interface for all the freezing and renaming options:

1.  **Input Font File:** Click to browse and select your input `.otf` or `.ttf` font file.
2.  **Output Font File:** Specify where to save the modified font (`[input_filename].featfreeze.otf` by default).
3.  **Options to control feature freezing:**
    *   **Features:** Enter a comma-separated list of OpenType feature tags (e.g., `smcp,c2sc,onum`). These are the features you want to "freeze."
    *   **Script:** Optionally, specify an OpenType script tag (e.g., `cyrl`, `latn`) to apply features only for that script. If blank, features are applied across all relevant scripts.
    *   **Lang:** Optionally, specify an OpenType language tag (e.g., `SRB ` for Serbian) to apply features for that specific language system.
    *   **Zap glyphnames...:** (Advanced, TTF only) Removes glyph names from the font, potentially reducing file size.
4.  **Options to control font renaming:**
    *   **Add a suffix to the font family name:** If checked, a suffix is added. By default, this suffix is constructed from the frozen feature tags (e.g., "MyFont SMCP C2SC").
    *   **Use a custom suffix...:** If the above is checked, you can specify your own suffix here (e.g., "SC").
    *   **Search for strings...:** Allows renaming parts of the font's internal names. Format: `search1/replace1,search2/replace2`.
    *   **Update font version string:** Adds information about the frozen features to the font's version string.
5.  **Reporting options:**
    *   **Report languages, scripts and features...:** Instead of modifying the font, this option prints out information about the features, scripts, and languages present in the input font.
    *   **Output names of remapped glyphs...:** Prints the names of glyphs that were changed during the freezing process.
    *   **Print additional information...:** Verbose mode, shows more details during processing.
6.  Click "Run" (or the equivalent button, often the program name itself at the bottom of the Gooey interface) to process the font.

The GUI includes a "Help" menu with links to "About" information and the project's online documentation.

#### Using the pyftfeatfreeze CLI

The basic command structure is:
```bash
pyftfeatfreeze [OPTIONS] INPATH [OUTPATH]
```

*   `INPATH`: Path to the input `.otf` or `.ttf` font file.
*   `OUTPATH`: Optional path for the output font file. If omitted, it defaults to `INPATH.featfreeze.otf`.

**Common CLI Options:**

*   `-f TAGS, --features TAGS`: Comma-separated OpenType feature tags (e.g., `'smcp,c2sc'`).
*   `-s SCRIPT, --script SCRIPT`: OpenType script tag (e.g., `cyrl`). If omitted, processing applies to all relevant scripts.
*   `-l LANG, --lang LANG`: OpenType language tag (e.g., `SRB `).
*   `-S, --suffix`: Add a suffix to font family name (derived from feature tags).
*   `-U SUFFIX, --usesuffix SUFFIX`: Use a custom suffix (e.g., `SC`) when `-S` is active.
*   `-R 'S/R,...', --replacenames 'S/R,...'`: Search and replace strings in font names (e.g., `'MyFont/MyFontNew,Regular/Reg'`).
*   `-z, --zapnames`: Zap glyph names from TTF fonts.
*   `-i, --info`: Update font version string.
*   `-r, --report`: Report font's features, scripts, languages instead of processing.
*   `-n, --names`: Output names of remapped glyphs.
*   `-v, --verbose`: Print detailed processing information.
*   `-V, --version`: Show program version.
*   `-h, --help`: Show help message with all options.

**CLI Examples:**

1.  **Freeze small caps and old-style numerals, add "SC OS" suffix, rename "OpenSans" to "OpenSansSC":**
    ```bash
    pyftfeatfreeze -f 'c2sc,smcp,onum' -S -U "SC OS" -R 'OpenSans/OpenSansSO' OpenSans-Regular.ttf OpenSansSO-Regular.ttf
    ```

2.  **Freeze Bulgarian localized forms (`locl` for Cyrillic script, Bulgarian language), add "BG" suffix:**
    ```bash
    pyftfeatfreeze -f 'locl' -s 'cyrl' -l 'BGR ' -S -U BG MyFont.otf MyFontBG.otf
    ```
    *Note: To remap features for multiple script/language combinations, run the tool multiple times, using the output of one run as the input for the next. Apply renaming options (`-S`, `-U`, `-R`) typically on the final run.*

3.  **Only rename parts of the font's internal name (no feature freezing):**
    ```bash
    pyftfeatfreeze -R 'Lato/Otal,Regular/Rg' Lato-Regular.ttf Otal-Rg.ttf
    ```

## Part 2: For Developers & Contributors

### How the Code Works (Internals)

The core logic resides in the `RemapByOTL` class within `src/opentype_feature_freezer/__init__.py`. The process flow is as follows:

1.  **Font Opening:** The input font file is opened using `fontTools.ttLib.TTFont`.
2.  **Feature and Lookup Filtering:**
    *   The tool identifies relevant GSUB (Glyph Substitution) lookups.
    *   It filters these lookups based on user-specified OpenType feature tags (`--features`), script tag (`--script`), and language tag (`--lang`).
    *   If no script is specified, the tool attempts to apply features across all relevant scripts by processing each script tag found. For language systems within a script, if a specific language is not given or does not match an existing `LangSysRecord`, the `DefaultLangSys` for that script is used.
3.  **Substitution Application:**
    *   It processes GSUB LookupType 1 (Single Substitution) and LookupType 3 (Alternate Substitution).
    *   It also handles LookupType 7 (Extension Substitution) which can wrap Type 1 or Type 3 lookups.
    *   A substitution mapping is built, tracking which original glyph names should be replaced by which new glyph names. For alternate substitutions, the first alternate glyph from the list is chosen (e.g., `a.alt1` from `[a.alt1, a.alt2]`).
4.  **`cmap` Remapping:**
    *   The font's character map (`cmap` table) is modified. Existing Unicode codepoints that pointed to original glyphs are updated to point to the new glyphs resulting from the applied substitutions. This is what makes the features "default."
5.  **Font Renaming (Optional):**
    *   If requested via options like `--suffix`, `--usesuffix`, or `--replacenames`, the tool modifies various name records in the `name` table (e.g., Family Name (ID 1), Full Name (ID 4), PostScript Name (ID 6), Version String (ID 5), Unique ID (ID 3), WWS Family/Subfamily (ID 16, 17)).
    *   For CFF-based OpenType fonts (`.otf`), it also updates `FamilyName`, `FullName`, and the main font name in the `CFF ` table.
6.  **Glyph Name Zapping (Optional):**
    *   For TrueType-flavored fonts (`.ttf`), the `--zapnames` option sets the `post` table format to 3.0. This removes glyph names from the font, which can sometimes reduce file size but makes debugging harder.
7.  **Font Saving:** The modified font object is saved to the output path using `fontTools.ttLib.TTFont.save()`.

**Key Modules:**

*   `src/opentype_feature_freezer/__init__.py`: Contains the `RemapByOTL` class with the primary font processing logic.
*   `src/opentype_feature_freezer/cli.py`: Implements the `pyftfeatfreeze` command-line interface using Python's `argparse` module. It parses arguments and passes them to `RemapByOTL`.
*   `app/OTFeatureFreezer.py`: Uses `ezgooey` to wrap the `argparse` definitions from `cli.py`, creating the `OTFeatureFreezer` GUI application for macOS and Windows.

**Limitations:**

*   **Supported Substitutions:** Primarily handles GSUB Single (Type 1) and Alternate (Type 3) substitutions, including those within Extension (Type 7) lookups. It does not process other GSUB lookup types like Ligature, Multiple, or Chaining Contextual substitutions.
*   **`cmap` Dependency:** The tool works by remapping existing `cmap` entries. If a glyph involved in a substitution (either the original or the replacement) does not have a Unicode value assigned in any `cmap` table, that specific remapping might not have a visible effect through standard character input. A warning is issued in such cases.
*   **Global Feature Application:** Features are applied based on the chosen script and language for the entire font. The tool does not interpret complex conditional logic within OpenType feature definitions themselves.

### Coding Rules & Conventions

*   **Python Version:** The codebase targets Python 3.6 and newer.
*   **Type Hinting:** Modern Python type hints are used throughout the code for improved clarity, maintainability, and to facilitate static analysis. See `typing` module usage.
*   **Logging:** The standard `logging` module is used for outputting informational messages, warnings, and errors. Verbosity is controlled by the `-v` flag.
*   **Project & Dependency Management:** [Poetry](https://python-poetry.org/) is used for managing dependencies, building the package, and publishing. Configuration is in `pyproject.toml`.
*   **Static Analysis:** [MyPy](http://mypy-lang.org/) is used for static type checking, with configuration in `mypy.ini`.
*   **Testing:** [pytest](https://pytest.org/) is used for unit and integration testing. Tests are located in the `tests/` directory.
*   **Code Style:** While no specific linter (like Flake8 or Black) is explicitly configured in `pyproject.toml` apart from MyPy, contributions should generally follow PEP 8 guidelines and maintain consistency with the existing codebase.

### Contributing

Contributions are welcome! Whether it's reporting a bug, suggesting an improvement, or submitting code changes.

**Reporting Issues:**

*   Please use the [GitHub Issues](https://github.com/twardoch/fonttools-opentype-feature-freezer/issues) page to report bugs or request features.
*   Provide clear steps to reproduce bugs, including the font file (if possible and license permits), the command used, and observed vs. expected behavior.

**Development Setup:**

1.  Ensure you have Python 3.6+ and [Poetry](https://python-poetry.org/docs/#installation) installed.
2.  Clone the repository:
    ```bash
    git clone https://github.com/twardoch/fonttools-opentype-feature-freezer.git
    ```
3.  Navigate into the project directory:
    ```bash
    cd fonttools-opentype-feature-freezer
    ```
4.  Install development dependencies, including `pytest` and `mypy`, in a virtual environment using Poetry:
    ```bash
    poetry install
    ```
5.  Activate the virtual environment:
    ```bash
    poetry shell
    ```

**Building:**

*   **Python Package (Wheel/sdist):**
    ```bash
    poetry build
    ```
    The distributable files will be in the `dist/` directory.

*   **GUI Applications (DMG for macOS, EXE for Windows):**
    *   Building these requires a macOS environment.
    *   Navigate to the `app/` subdirectory.
    *   Run the deployment script:
        ```bash
        cd app
        ./macdeploy all
        ```
    *   This script uses PyInstaller and other tools to package the GUI application.

**Running Tests:**

*   Ensure you have installed development dependencies (`poetry install`).
*   Run `pytest` from the project root directory:
    ```bash
    pytest
    ```
    Or, if your environment is not yet active:
    ```bash
    poetry run pytest
    ```

## Other Information

### Software License and Disclaimer

This tool is licensed "as is" under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). By using the tool, you accept all conditions of the license, including Disclaimer of Warranty and Limitation of Liability.

**Important:** When modifying fonts, please ensure you comply with the font's End User License Agreement (EULA). If the font is licensed under the SIL Open Font License (OFL) and uses Reserved Font Name(s), you **must** use the `-R` (rename) option to change the font's name if you plan to distribute the modified version.

### Requirements

*   Python 3.6 or newer.
*   [fontTools](https://github.com/fonttools/fonttools/) (automatically installed as a dependency).
*   For the GUI (OTFeatureFreezer): [ezgooey](https://github.com/chriskiehl/Gooey) (automatically installed).

### Changelog (Recent Highlights)

*   **1.32.2 (and recent versions):** Ongoing type hinting improvements, CI updates, and minor bug fixes.
*   **1.32:** Changed the `-s` (script) option: if not provided, remapping attempts to apply to all relevant scripts.
*   **1.31:** Changed the `-S` (suffix) option: if not provided, no suffix is added. Introduced GUI apps.

*For older history, this tool was previously part of the `fonttools-utils` repository.*

### Credits

*   Original code and ongoing development by Adam Twardoch.
*   Contributions from various developers (see `AUTHORS` and `CONTRIBUTORS` files, and GitHub commit history).
*   Built upon the powerful `fontTools` library.

---

<!-- GitHub Buttons (optional, from original README) -->
<p align="center">
  <a class="github-button" href="https://github.com/twardoch/fonttools-opentype-feature-freezer" data-icon="octicon-star" data-size="large" data-show-count="true" aria-label="Star twardoch/fonttools-opentype-feature-freezer on GitHub">Star</a>
  <a class="github-button" href="https://github.com/twardoch/fonttools-opentype-feature-freezer/subscription" data-icon="octicon-eye" data-size="large" data-show-count="true" aria-label="Watch twardoch/fonttools-opentype-feature-freezer on GitHub">Watch</a>
  <a class="github-button" href="https://github.com/twardoch/fonttools-opentype-feature-freezer/fork" data-icon="octicon-repo-forked" data-size="large" data-show-count="true" aria-label="Fork twardoch/fonttools-opentype-feature-freezer on GitHub">Fork</a>
</p>
<!-- Place this tag in your head or just before your close body tag. -->
<script async defer src="https://buttons.github.io/buttons.js"></script>
