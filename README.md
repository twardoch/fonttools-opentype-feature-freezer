# OpenType Feature Freezer

With **[OpenType Feature Freezer](https://twardoch.github.io/fonttools-opentype-feature-freezer/)**, you can “freeze” some OpenType features into a font.

These features are then “on by default”, so characters previously accessible through OpenType features only (such as smallcaps, oldstyle numerals or localized forms) will now be accessible even in apps that don’t support OpenType features, such as LibreOffice, OpenOffice, or in apps that don’t support a particular feature, such as Microsoft Office in case of smallcaps.

_Note: This tool actually remaps the `cmap` table of the font by applying the specified `GSUB` features. It will not work for substitutions where neither glyph has any `cmap` entries. Only single and alternate substitutions are supported._

This tool comes in two versions: **OTFeatureFreezer**: a simple GUI (graphical) app for macOS and Windows that you can download and run without any special perparations, and **pyftfeatfreeze**: a CLI (command-line) app that required Python 3.6 or newer to be installed on your computer.

Current version: **[1.32.0](https://github.com/twardoch/fonttools-opentype-feature-freezer/blob/master/README.md#changelog)**

- [Download and install](https://twardoch.github.io/fonttools-opentype-feature-freezer/)
- [Documentation](https://github.com/twardoch/fonttools-opentype-feature-freezer/blob/master/README.md#documentation)
- [Source code](https://github.com/twardoch/fonttools-opentype-feature-freezer/)
- [Issues](https://github.com/twardoch/fonttools-opentype-feature-freezer/issues) for problem reporting

# Installation

## Install the OTFeatureFreezer GUI app for macOS

### <a class="github-button btn btn-primary" href="https://github.com/twardoch/fonttools-opentype-feature-freezer/raw/master/download/OTFeatureFreezer.dmg" data-color-scheme="no-preference: dark; light: dark; dark: dark;" data-icon="octicon-download" data-size="large" aria-label="Download DMG for macOS">Download DMG for macOS</a>

1. On **macOS**, click the **Download** link above.
2. **Ctrl+click** the downloaded DMG, choose **Open**, then **Open** again.
3. Drag the _OTFeatureFreezer.app_ icon to your **/Applications** folder.
4. When you **run the app for the first time**, **Ctrl+click** the _OTFeatureFreezer.app_, choose **Open**, then click **Open**.
5. Later, you can just double-click the icon to run the app. If the app does not run, double-click again.
6. See the [Documentation](https://github.com/twardoch/fonttools-opentype-feature-freezer/blob/master/README.md#documentation) for info about how to use the GUI app. The GUI corresponds to the command-line options.

## Install the OTFeatureFreezer GUI app for Windows (64-bit)

### <a class="github-button btn btn-primary" href="https://github.com/twardoch/fonttools-opentype-feature-freezer/raw/master/download/OTFeatureFreezer.zip" data-color-scheme="no-preference: dark; light: dark; dark: dark;" data-icon="octicon-download" data-size="large" aria-label="Download ZIP for Windows">Download ZIP for Windows</a>

1. You need a **64-bit** version of **Windows**, 7 or newer. 32-bit Windows is not supported.
2. Click the **Download** link above.
3. Unzip the downloaded ZIP.
4. Double-click the _setup_featfreeze.exe_ icon to install the app.
5. Run _OTFeatureFreezer_ from your Start menu.
6. See the [Documentation](https://github.com/twardoch/fonttools-opentype-feature-freezer/blob/master/README.md#documentation) for info about how to use the GUI app. The GUI corresponds to the command-line options.

## Install the pyftfeatfreeze CLI app

This tool requires Python 3.6 or above to be installed first. Get it from https://www.python.org or your package manager.

### Recommended

We recommend using [pipx](https://pypi.org/project/pipx/) to install Python command line tools. Pipx tucks them away neatly on your computer and gives you an easy way to add, update and remove Python tools on all platforms, without leaving a mess in your Python installation.

```
pipx install opentype-feature-freezer
```

### Other methods

Install it with `pip`, as any other Python package.

```
# This is best done inside a virtual environment, so you don't pollute
# your Python installation and need no special privileges to install anything.

pip install --upgrade opentype-feature-freezer
```

If this does not work, try:

```
python3 -m pip install --user --upgrade opentype-feature-freezer
```

### Development version

```
pip install --upgrade git+https://github.com/twardoch/fonttools-opentype-feature-freezer
```

If this does not work, use:

```
python3 -m pip install --user --upgrade git+https://github.com/twardoch/fonttools-opentype-feature-freezer
```

- You may need to do `pip install --upgrade configparser` before installing

# Documentation

## Examples

Let’s say you have the font *CharisSIL-R.ttf* (with the menu name “Charis SIL”), and this font includes true smallcaps accessible via the OpenType Layout features `c2sc` (for uppercase) and `smcp` (for lowercase). Let’s say that you’d like to make a second font where the **true smallcaps** are available by default. Just run:

```
pyftfeatfreeze -f 'c2sc,smcp' -S -U SC -R 'Charis SIL/Charix,CharisSIL/Charix' CharisSIL-R.ttf CharixSC-R.ttf
```

You’ll get a new font *CharisSIL-R.ttf* (with the menu name “Charix SC”). This font will have smallcaps instead of the lowercase and uppercase letters, available in all apps.

Since the “Charis SIL” font is licensed under the OFL, and uses the Reserved Font Names “Charis” and “SIL”, I’ve specified the `-R` option to replace the name strings `Charis SIL` and `CharisSIL` with `Charix`. This way, the modified font is compliant with the OFL and I can distribute it.

The following example remaps the font so that the **Bulgarian localized forms** are available by default in all apps (the suffix “BG” will be added to the menu name):

```
pyftfeatfreeze -f 'locl' -s 'cyrl' -l 'BGR ' -S -U BG SomeFont.ttf SomeFontBG.ttf
```

*Note: To remap features from multiple scripts or languagesystems, run the tool multiple times (taking the previous run’s output as input). Use the `-S` option only on the final run.*

The following replaces the string `Lato` by `Otal` in all internal font names (in the `name` and `CFF ` tables), without doing any “feature freezing”. This can be used to quickly change some internal font names:

```
pyftfeatfreeze -R 'Lato/Otal' Lato-Regular.ttf Otal-Regular.ttf
```


## Command-line syntax

```
usage: pyftfeatfreeze [-h] [-f FEATURES] [-s SCRIPT] [-l LANG] [-z] [-S]
                      [-U USESUFFIX] [-R REPLACENAMES] [-i] [-r] [-n] [-v]
                      [-V]
                      inpath [outpath]

With pyftfeatfreeze you can "freeze" some OpenType features into a font. These
features are then "on by default", even in apps that don't support OpenType
features. Internally, the tool remaps the "cmap" table of the font by applying
the specified GSUB features. Only single and alternate substitutions are
supported.

positional arguments:
  inpath                input .otf or .ttf font file
  outpath               output .otf or .ttf font file (optional)

optional arguments:
  -h, --help            show this help message and exit

options to control feature freezing:
  -f FEATURES, --features FEATURES
                        comma-separated list of OpenType feature tags, e.g.
                        'smcp,c2sc,onum'
  -s SCRIPT, --script SCRIPT
                        OpenType script tag, e.g. 'cyrl' (default: 'latn')
  -l LANG, --lang LANG  OpenType language tag, e.g. 'SRB ' (optional)
  -z, --zapnames        zap glyphnames from the font ('post' table version 3,
                        .ttf only)

options to control font renaming:
  -S, --suffix          add a suffix to the font family name (by default, the
                        suffix will be constructed from the OpenType feature
                        tags)
  -U USESUFFIX, --usesuffix USESUFFIX
                        use a custom suffix when --suffix is provided
  -R REPLACENAMES, --replacenames REPLACENAMES
                        search for strings in the font naming tables and
                        replace them, format is
                        'search1/replace1,search2/replace2,...'
  -i, --info            update font version string

reporting options:
  -r, --report          report languages, scripts and features in font
  -n, --names           output names of remapped glyphs during processing
  -v, --verbose         print additional information during processing
  -V, --version         show program's version number and exit

Examples: pyftfeatfreeze -f 'c2sc,smcp' -S -U SC OpenSans.ttf OpenSansSC.ttf
pyftfeatfreeze -R 'Lato/Otal' Lato-Regular.ttf Otal-Regular.ttf
```

*Tip: the `-n` option outputs a space-separated list of “frozen” glyphs. If you redirect it to a file, you can use this list as input for `pyftsubset` to create a small font that only includes the “frozen” glyphs.*

## Other

### Problem reporting

To report a problem, open an **[issue](https://github.com/twardoch/fonttools-opentype-feature-freezer/issues)**. You need a Github account.

### Software license and disclaimer

This tool is licensed “as is” under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). By using the tool, you accept all conditions of the license, including Disclaimer of Warranty and Limitation of Liability. **If you use this tool, please consult if your font’s EULA allows modifications. If the font is licensed under the OFL and uses the Reserved Font Name, please use the `-R` option to change the Reserved Font Name to something else.**


### Requirements

This tool is written for Python 3.6+, and uses [fontTools/TTX](https://github.com/fonttools/fonttools/).


### Changelog

- **1.32.0**: Changes the `-s` (script) option so that if it’s not provided, the remapping is in all scripts.
- **1.31.0**: Changes the `-S` (suffix) option so that if it’s not provided, no sufix is added, and added the GUI apps.
- Previously, this tool was published as a sub-tool in a [fonttools-utils](https://github.com/twardoch/fonttools-utils/tree/master/pyftfeatfreeze) repo
- The other tools of the `fonttools-utils` repo are now at [fonttools-ttxjson](https://github.com/twardoch/fonttools-ttxjson) and [mac-os-x-system-font-replacer](https://github.com/twardoch/mac-os-x-system-font-replacer)

### Building

#### Python

To build the Python package, install [Poetry](https://python-poetry.org/):

```
pip install poetry
```

or

```
python3 -m install --user --upgrade poetry
```

then in the main folder of the project run:

```
poetry build
```

#### DMG & EXE

To build the DMG & EXE, you need macOS. In the [app](https://github.com/twardoch/fonttools-opentype-feature-freezer/tree/master/app) subfolder, run `./macdeploy all`

### Credits

* Code by [Adam Twardoch and others](https://raw.githubusercontent.com/twardoch/fonttools-opentype-feature-freezer/master/AUTHORS)

<!-- Place this tag in your head or just before your close body tag. -->
<script async defer src="https://buttons.github.io/buttons.js"></script>

