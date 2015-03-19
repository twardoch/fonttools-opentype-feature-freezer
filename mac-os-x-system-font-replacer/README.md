MacOSXSystemFontReplacer
========================

With **MacOSXSystemFontReplacer** v1.0, you can replace your system UI fonts of
Mac OS X 10.10 Yosemite with any fonts of your choice. 

You can supply any fonts to the tool as long as they have filenames in
a format that the tool expects. 

The tool is “safe” i.e. it does not modify the original system UI fonts. Instead, it writes patched versions of the fonts you provide into the System library folder, but you can easily uninstall those later manually or using the tool itself. Also, since it uses the fontTools library, it only does minimal modifications to your fonts, retaining all essential information. The fonts that you want patched can be in ```.ttf``` or ```.otf``` format, but you need to rename them and use the ```.otf``` extension. 

**If you use this tool, please consult if your font’s EULA allows modifications. Since this tool copies a small bit of the OS X system font into the patched fonts, you should not redistribute the patched fonts.** 

![Example: Work Sans](example-work-sans.png?raw=true "Example: I have used the tool to replace the default UI system font with Work Sans")
*This example shows how the tool was used to replace the default UI system fonts of Mac OS X 10.10 with the open-source [Work Sans](http://weiweihuanghuang.github.io/Work-Sans/) font family. The ```-s 105``` option was used to visually increase the font sizes by 5%.*

Installation and basic usage
----------------------------
This is a command-line tool written in Python. 

1. Download and install¹ [fontTools/TTX](https://github.com/behdad/fonttools/)
2. Download **[MacOSXSystemFontReplacer.py](./MacOSXSystemFontReplacer.py?raw=true)** and save it in a folder
3. Place your fonts in the same folder
3. Rename your fonts to a scheme that the tool expects (see section “Preparing your fonts” below)
4. Run Terminal.app and navigate to that folder using ```cd```
5. Run ```sudo python ./MacOSXSystemFontReplacer.py``` 
6. Enter your OS X Administrator password
7. Log out of Mac OS X and log in again

¹To install **fontTools/TTX**: download the [fonttools-master.zip](https://github.com/behdad/fonttools/archive/master.zip?raw=true) archive, unzip it, open Terminal.app and navigate to the unzipped folder using ```cd```. Then just type ```sudo python setup.py install``` and enter your Administrator password. 

Advanced usage
--------------
There are more options to the tool: 
```
MacOSXSystemFontReplacer.py [-h] [-i INPUT_FOLDER] [-s FONT_SIZE]
                            [-o OUTPUT_FOLDER] [-H] [-u] [-c]
                            [-t SYSTEM_TTC]

  -h, --help            show this help message and exit
  -i INPUT_FOLDER, --input-folder INPUT_FOLDER
                        path to folder with your input font files, default is
                        /Users/adam/Developer/vcs/github/twardoch/fonttools-
                        utils/mac-os-x-system-font-replacer
  -s FONT_SIZE, --font-size FONT_SIZE
                        scale the relative font size in %, default is 100, use
                        a higher value such as 105 to optically increase your
                        patched UI fonts
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                        custom path to folder where your patched fonts will be
                        installed, default is /Library/Fonts/ and you should
                        run the tool as: sudo MacOSXSystemFontReplacer.py
  -H, --help-more       print the file names that the tool expects to find in
                        the -i INPUT_FOLDER
  -u, --uninstall       uninstall previously patched fonts from the system folder 
                        or the -o OUTPUT_FOLDER
  -c, --no-reset-caches
                        do not reset OS X font caches (useful if you are
                        testing and using a custom -o OUTPUT_FOLDER)
  -t SYSTEM_TTC, --system-ttc SYSTEM_TTC
                        custom path to
                        /System/Library/Fonts/HelveticaNeueDeskInterface.ttc
                        (which may be different from current default in future
                        versions of OS X)
```

Preparing your fonts
--------------------

If you wish to replace all system UI fonts of Mac OS X 10.10 Yosemite with your custom fonts, you need to **rename the font files exactly** so that each of your font files has one of file names given in the table below. The table also indicates the general usage of the font and the relationships in the design of the original system font family. 

Filename | Usage | Design
---------| ------| ------
**System Font Regular.otf** | menus and other widgets | the main UI font
**System Font Bold.otf** | app menu and other emphasis | bolder version of Regular
**System Font Italic.otf** | emphasis | italic version of Regular
**System Font Bold Italic.otf** | | Bold Italic version of Regular
**System Font Medium P4.otf** | notification titles | slightly bolder than Regular
**System Font Medium Italic P4.otf** | emphasis of above | slightly bolder than Italic
**System Font UltraLight.otf** | largest headlines¹ | thinnest
**System Font Thin.otf** | mid-sized headlines² | slightly bolder than UltraLight
**System Font Light.otf** | yet smaller headlines³ | slightly bolder than Thin
**System Font Heavy.otf** | | bolder than Bold

¹e.g. in Calendar for month ²e.g. in the headline of Notification Center ³or as bold for the UltraLight e.g. in Calendar for year

You need to place the font files renamed according to the above scheme in a folder, and then you need to specify that folder using the ```-i``` command-line option. (If the tool is in the same folder as the fonts, you can omit that option). The tool will match each of your fonts to one of the default Mac OS X UI fonts using the filename. 

Then it will try to patch your fonts and install them in ```/Library/Fonts/```. Then you **log out and back in**, and you should see your new UI fonts.

Notes
-----

Please use the file names exactly as provided, and **use the ```.otf``` extension** even if your fonts are actually ```.ttf```. 

The most important fonts are *System Font Regular.otf* and *System Font Bold.otf*. You don’t need to provide all fonts (then the default system font will still be used in some places). 

If you find that after logging out and in again, the new UI fonts are visually too small, run the tool again, but this time, provide an ```-s``` command-line option with a percentage scaling. Usually a value such as ```-s 105``` will be good enough. 

In Mac OS X 10.10 Yosemite, the default Mac OS X UI fonts are stored in ```/System/Library/Fonts/HelveticaNeueDeskInterface.ttc```. The tool allows you to point to a different ```.ttc``` font as default, so it should work even in newer OS X versions. 

Software License and Disclaimer
-------------------------------
This tool is licensed “as is” under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). By using the tool, you accept all conditions of the license, including Disclaimer of Warranty and Limitation of Liability.

Requirements
------------

This tool is written in Python 2.7 and requires the fontTools/TTX package from https://github.com/behdad/fonttools/

Credits
-------
* Code by: [Adam Twardoch](./AUTHORS) 
* Inspired by https://github.com/jenskutilek/FiraSystemFontReplacement and https://github.com/dtinth/YosemiteSystemFontPatcher 
* Homepage: https://github.com/twardoch/fonttools-utils/tree/master/mac-os-x-system-font-replacer
