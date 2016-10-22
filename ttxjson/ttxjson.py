#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

VERSION = "1.00"
"""ttxjson.py
Version %(version)s
Copyright (c) 2016 by Adam Twardoch <adam@twardoch.com>
Licensed under the Apache 2 license.
""" % {"version": VERSION}

# fontTools gives access to internal SFNT font structures
# INSTALL
# pip install --user git+https://github.com/fonttools/fonttools.git
import fontTools.ttLib

def ttxJson(font, tables=None): 
	# jsonpickle is a module that converts a more complex Python
	# data structure to a JSON string, and back
	# https://jsonpickle.github.io/
	# INSTALL
	# pip install --user git+https://github.com/jsonpickle/jsonpickle.git
	import jsonpickle

	if not tables: 
		tables = set(font.keys())
	# To create a jsonString Pythonvia jsonpickle, we need first to iterate through 
	# each font table to force decompilation from SFNT into Pythonic object structures. 
	# The tables which are not decompiled will be jsonpickled as base64 SFNT blocks.
	# ** Is there a better method? ** 
	templist = [font[tag] for tag in tables]

	# We jsonpickle.encode the font into jsonString
	jsonString = jsonpickle.encode(font)
	return jsonString

def main():
	import os.path
	import sys
	from argparse import ArgumentParser
	# json is a built-in Python module that allows simple conversion
	# between JSON strings and Python dicts
	# https://docs.python.org/2/library/json.html
	import json

	parser = ArgumentParser()
	parser.description = """
	%(prog)s is a Python tool that converts an SFNT font (OTF, TTF) into JSON. 
	Homepage: https://github.com/twardoch/fonttools-utils/
	"""	
	parser.add_argument('infontpath', help='Input SFNT font file (.otf, .ttf)')
	parser.add_argument('-o', '--output', help='Output JSON path, stdout if not given')
	parser.add_argument('-t', '--tables', help='Comma-separated list of SFNT tables, e.g. CFF,head,name')
	args = vars(parser.parse_args())
	# Get a font path and output JSON path
	if args['infontpath']: 
		fontPath = args['infontpath']
		if not os.path.exists(fontPath): 
			print("%s does not exist" % (fontPath), file=sys.stderr)
			sys.exit(-2)
	else: 
		parser.print_help()
		sys.exit(0)

	# Create fontTools font object
	font = fontTools.ttLib.TTFont(fontPath, lazy=False, ignoreDecompileErrors=True)

	# Get an optional list of comma-separated SFNT tables to decompile
	# as in "CFF,name,fvar"
	if args['tables']: 
		todotables = args['tables'].split(",")
		tables = set([tag.ljust(4) for tag in todotables]) & set(font.keys())
	else: 
		tables = set(font.keys())

	# We get the JSON representation of the font 
	jsonString = ttxJson(font, tables)
	# We load it into a Python dict via json.loads
	jsonDict = json.loads(jsonString)
	# We dump the Python dict into a jsonFormatted string
	jsonFormatted = json.dumps(jsonDict, sort_keys=True, indent=2)
	# We write the jsonFormatted string into jsonPath
	if args['output']: 
		jsonFile = file(args['output'], "w")
	else: 
		jsonFile = sys.stdout
	print(jsonFormatted, file=jsonFile)

	# Example using jsonDict: 
	# upm = jsonDict[u'tables'][u'head'][u'unitsPerEm']

if __name__ == "__main__":
	main()
