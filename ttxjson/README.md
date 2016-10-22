ttxjson
=======

**ttxjson** is a Python tool that converts an SFNT font (OTF, TTF)
into JSON, using the [`fontTools`](https://github.com/fonttools/fonttools/) and [`jsonpickle`](https://github.com/jsonpickle/jsonpickle) Python modules.

Installation on Mac OS X
------------------------
* Download and unzip https://github.com/twardoch/fonttools-utils/archive/master.zip
* Open Terminal and navigate to the folder where you’ve unzipped the archive.
* Type these lines one by one, enter the Administrator password after the first "sudo" line: 
```
pip install --user git+https://github.com/fonttools/fonttools.git
pip install --user git+https://github.com/jsonpickle/jsonpickle.git
cd ttxjson
chmod gou+x pyftfeatfreeze.py
sudo mkdir -p /usr/local/bin
sudo cp pyftfeatfreeze.py /usr/local/bin
```
* Test if the tool is available in Terminal by typing `ttxjson.py -h`

Command-line syntax
-------------------
```
usage: ttxjson.py [-h] [-o OUTPUT] [-t TABLES] infontpath

ttxjson.py is a Python tool that converts an SFNT font (OTF, TTF) into JSON.
Homepage: https://github.com/twardoch/fonttools-utils/

positional arguments:
  infontpath            Input SFNT font file (.otf, .ttf)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output JSON path, stdout if not given
  -t TABLES, --tables TABLES
                        Comma-separated list of SFNT tables, e.g.
                        CFF,head,name
```

Python usage
------------

```python
import ttxjson
import fontTools.ttLib
font = fontTools.ttLib.TTFont(fontPath, lazy=False, ignoreDecompileErrors=True)
json = ttxjson.ttxJson(font, tables=['head','name','CFF '])
print json
```

Software License and Disclaimer
-------------------------------
This tool is licensed “as is” under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). By using the tool, you accept all conditions of the license, including Disclaimer of Warranty and Limitation of Liability. **If you use this tool, please consult if your font’s EULA allows modifications. If the font is licensed under the OFL, please use the `-R` option to change the Reserved Font Name to something else.** 

Requirements
------------
This tool is written in Python 2.7 and requires [`fontTools`](https://github.com/fonttools/fonttools/) and [`jsonpickle`](https://github.com/jsonpickle/jsonpickle). 

Credits
-------
* Code by [Adam Twardoch](./AUTHORS) 
* Homepage: [https://github.com/twardoch/fonttools-utils/](https://github.com/twardoch/fonttools-utils/)