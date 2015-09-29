pyftfeatfreeze
==============

With **pyftfeatfreeze**, you can “freeze” some OpenType features into a font. 

These features are then “on by default”, so characters previously accessible through OpenType featureso only (such as smallcaps, oldstyle numerals or localized forms) will now be accessible even in apps that don’t support OpenType features, such as LibreOffice, OpenOffice, or in apps that don’t support a particular feature, such as Microsoft Office in case of smallcaps. 

*Note: This tool actually remaps the `cmap` table of the font by applying the specified `GSUB` features. Only single and alternate substitutions are supported.*

Installation on Mac OS X
------------------------
* Download and unzip https://github.com/twardoch/fonttools-utils/archive/master.zip
* Open Terminal and navigate to the folder where you’ve unzipped the archive.
* Type these lines one by one, enter the Administrator password after the first "sudo" line: 
```
cd pyftfeatfreeze
chmod gou+x pyftfeatfreeze.py
sudo mkdir -p /usr/local/bin
sudo cp pyftfeatfreeze.py /usr/local/bin
```
* Test if the tool is available in Terminal by typing `pyftfeatfreeze.py -h`

Examples
--------
Let’s say you have the font *CharisSIL-R.ttf* (with the menu name “Charis SIL”), and this font includes true smallcaps accessible via the OpenType Layout features `c2sc` (for uppercase) and `smcp` (for lowercase). Let’s say that you’d like to make a second font where the **true smallcaps** are available by default. Just run: 
```
pyftfeatfreeze.py -f 'c2sc,smcp' -S -U SC -R 'Charis SIL/Charix,CharisSIL/Charix' CharisSIL-R.ttf CharixSC-R.ttf
```
You’ll get a new font *CharisSIL-R.ttf* (with the menu name “Charix SC”). This font will have smallcaps instead of the lowercase and uppercase letters, available in all apps. 

Since the “Charis SIL” font is licensed under the OFL, and uses the Reserved Font Names “Charis” and “SIL”, I’ve specified the `-R` option to replace the name strings `Charis SIL` and `CharisSIL` with `Charix`. This way, the modified font is compliant with the OFL and I can distribute it. 

The following example remaps the font so that the **Bulgarian localized forms** are available by default in all apps (the suffix “BG” will be added to the menu name): 
```
pyftfeatfreeze.py -f 'locl' -s 'cyrl' -l 'BGR ' -S -U BG SomeFont.ttf SomeFontBG.ttf
```

*Note: To remap features from multiple scripts or languagesystems, run the tool multiple times (taking the previous run’s output as input). Use the `-S` option only on the final run.*

The following replaces the string `Lato` by `Otal` in all internal font names (in the `name` and `CFF ` tables), without doing any “feature freezing”. This can be used to quickly change some internal font names: 
```
pyftfeatfreeze.py -R 'Lato/Otal' Lato-Regular.ttf Otal-Regular.ttf
```

Command-line syntax
-------------------
```
usage: pyftfeatfreeze.py [options] inpath [outpath]

With pyftfeatfreeze.py you can "freeze" some OpenType features into a font.
These features are then "on by default", even in apps that don't support
OpenType features. This tool actually remaps the "cmap" table of the font by
applying the specified GSUB features. Only single and alternate substitutions
are supported. Homepage: https://github.com/twardoch/fonttools-utils/

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
  -S, --suffix          add a suffix to the font menu names (by default, the
                        suffix will be constructed from the OpenType feature
                        tags)
  -U USESUFFIX, --usesuffix USESUFFIX
                        use a custom suffix when -S is provided
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

Examples: 
pyftfeatfreeze.py -f 'c2sc,smcp' -S -U SC OpenSans.ttf OpenSansSC.ttf
pyftfeatfreeze.py -R 'Lato/Otal' Lato-Regular.ttf Otal-Regular.ttf
```

*Tip: the `-n` option outputs a space-separated list of “frozen” glyphs. If you redirect it to a file, you can use this list as input for `pyftsubset` to create a small font that only includes the “frozen” glyphs.*

Software License and Disclaimer
-------------------------------
This tool is licensed “as is” under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). By using the tool, you accept all conditions of the license, including Disclaimer of Warranty and Limitation of Liability. **If you use this tool, please consult if your font’s EULA allows modifications. If the font is licensed under the OFL, please use the `-R` option to change the Reserved Font Name to something else.** 

Requirements
------------
This tool is written in Python 2.7 and requires [fontTools/TTX](https://github.com/behdad/fonttools/). 

Credits
-------
* Code by [Adam Twardoch](./AUTHORS) 
* Homepage: [https://github.com/twardoch/fonttools-utils/](https://github.com/twardoch/fonttools-utils/)