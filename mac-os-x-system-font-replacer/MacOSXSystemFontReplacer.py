#!/usr/bin/env python
# -*- coding: utf-8 -*-

VERSION = "1.0"
"""MacOSXSystemFontReplacer.py
Version %(version)s
Copyright (c) 2015 by Adam Twardoch <adam@twardoch.com>
Licensed under the Apache 2 license.
""" % {"version": VERSION}
import argparse
import os
import os.path
import fontTools.ttLib
import subprocess

parser = argparse.ArgumentParser()
parser.description = """With %(prog)s v""" + VERSION + """, 
you can replace your system UI fonts of Mac OS X 10.10 Yosemite with any fonts 
of your choice. You can supply any fonts to the tool as long as they have filenames in a format that 
the tool expects. Please run %(prog)s -H for the exact file names you should provide. The tool is 'safe' i.e. 
it does not modify the original system UI fonts. Instead, it writes patched versions of the fonts you 
provide into the System library folder, but you can easily uninstall those later manually or using the tool itself. 
"""
parser.add_argument("-i", "--input-folder", 
	help="path to folder with your input font files, default is %(default)s", 
	default=os.getcwd()
	)
parser.add_argument("-s", "--font-size", 
	help="scale the relative font size in %%, default is %(default)s, use a higher value such as 105 to optically increase your patched UI fonts", 
	type=int, 
	default=100
	)
parser.add_argument("-o", "--output-folder", 
	help="custom path to folder where your patched fonts will be installed, default is %(default)s and you should run the tool as: sudo %(prog)s", 
	default="/Library/Fonts/"
	)
parser.add_argument("-H", "--help-more", 
	help="print the file names that the tool expects to find in the -i INPUT_FOLDER", 
 	action="store_true", 
 	default=False
 	)
parser.add_argument("-u", "--uninstall", 
	help="uninstall previously patched fonts from system folder or the -o OUTPUT_FOLDER", 
 	action="store_true", 
 	default=False
	)
parser.add_argument("-c", "--no-reset-caches", 
	help="do not reset OS X font caches (useful if you are testing and using a custom -o OUTPUT_FOLDER)", 
 	action="store_true", 
 	default=True
 	)
parser.add_argument("-t", "--system-ttc", 
	help="custom path to %(default)s (which may be different from current default in future versions of OS X)", 
	default="/System/Library/Fonts/HelveticaNeueDeskInterface.ttc"
	)
args = parser.parse_args()

def patchFont(ttcPath, fontNumber, inFolder, outFolder, help, fontScale, uninstall): 
	success = False
	try: 
		ttxIn = fontTools.ttLib.TTFont(ttcPath, fontNumber = fontNumber)
	except fontTools.ttLib.TTLibError: 
		ttxIn = None
	if ttxIn: 
		fontName = ""
		nameRecord = ttxIn["name"].getName(4, 1, 0, 0)
		if nameRecord: 
			fontName = nameRecord.string
		else: 
			nameRecord = ttxIn["name"].getName(4, 0, 3, 0)
			if nameRecord: 
				fontName = unicode(nameRecord.string, 'utf-16-be').encode('utf-8') 
		if help: 
			print('"%s.otf"' % fontName)
		elif uninstall: 
			fontPathOut = os.path.join(outFolder, "%s.otf" % (fontName))
			if os.path.exists: 
				try: 
					os.remove(fontPathOut)
					print("Uninstalled: %s" % (fontPathOut))
					success = True
				except: 
					print("Cannot uninstall: %s (try running tool with 'sudo'!)" % (fontPathOut))
		else: 
			fontPath = os.path.join(inFolder, "%s.otf" % (fontName))
			if os.path.exists(fontPath): 
				ttxOut = fontTools.ttLib.TTFont(fontPath)
				scaleFactor = (float(ttxOut["head"].unitsPerEm)/ttxIn["head"].unitsPerEm)/fontScale

				ttxOut["OS/2"].sTypoAscender = int(ttxIn["OS/2"].sTypoAscender * scaleFactor + 0.5)
				ttxOut["OS/2"].sTypoDescender = int(ttxIn["OS/2"].sTypoDescender * scaleFactor + 0.5)
				ttxOut["OS/2"].sTypoLineGap = int(ttxIn["OS/2"].sTypoLineGap * scaleFactor + 0.5)
				ttxOut["OS/2"].usWinAscent = int(ttxIn["OS/2"].usWinAscent * scaleFactor + 0.5)
				ttxOut["OS/2"].usWinDescent = int(ttxIn["OS/2"].usWinDescent * scaleFactor + 0.5)
				ttxOut["hhea"].ascent = int(ttxIn["hhea"].ascent * scaleFactor + 0.5)
				ttxOut["hhea"].descent = int(ttxIn["hhea"].descent * scaleFactor + 0.5)
				ttxOut["hhea"].lineGap = int(ttxIn["hhea"].lineGap * scaleFactor + 0.5)

				ttxOut["name"] = ttxIn["name"]
				ttxOut["head"].unitsPerEm = int(ttxOut["head"].unitsPerEm / fontScale + 0.5)
				if "CFF " in ttxOut: 
					cff = ttxOut["CFF "].cff
					cffd = cff[cff.fontNames[0]].rawDict
					cffd["FontMatrix"][0] = cffd["FontMatrix"][0] * fontScale
					cffd["FontMatrix"][3] = cffd["FontMatrix"][3] * fontScale
					psName = None
					psNameRecord = ttxIn["name"].getName(6, 1, 0, 0)
					if psNameRecord: 
						psName = psNameRecord.string
					else: 
						psNameRecord = ttxIn["name"].getName(6, 0, 3, 0)
						if psNameRecord: 
							psName = unicode(psNameRecord.string, 'utf-16-be').encode('utf-8') 
					if psName: 
						cff.fontNames[0] = psName
				fontPathOut = os.path.join(outFolder, "%s.otf" % (fontName))
				try: 
					ttxOut.save(fontPathOut)
					print('Saved patched: "%s"' % (fontPathOut))
					success = True
				except: 
					print("Cannot save: %s (try running tool with 'sudo'!)" % (fontPathOut))
			else: 
				print('Not found: "%s"' % (fontPath))
	return (ttxIn, success)

if args.help_more: 
	print("This tool expects your font files with the following file names to be present in\n%s :" % (args.input_folder))

fontNumber = 0
patchedFonts = 0
while True: 
	(opened, patched) = patchFont(ttcPath = args.system_ttc, fontNumber = fontNumber, inFolder = args.input_folder, outFolder = args.output_folder, help = args.help_more, fontScale = float(args.font_size)/100, uninstall = args.uninstall)
	if opened: 
		fontNumber += 1
	else: 
		break
	if patched: 
		patchedFonts += 1

if args.help_more: 
	print("The tool will match each of your fonts to one of the internal Mac OS X UI fonts\n(stored in %s)\nusing the filename.\nThen it will try to patch your fonts and install them in %s.\nAfter logging out and back in, you should see your new UI fonts." % (args.system_ttc, args.output_folder))
else: 
	if args.uninstall: 
		print("Uninstalled %d fonts" % (patchedFonts))
	else: 
		print("Finished patching %d fonts" % (patchedFonts))
if not args.no_reset_caches: 
	subprocess.call(["sudo","atsutil","databases","-remove"])
	print("Mac OS X font caches have been reset. Please log out of Mac OS X and log in again.")
