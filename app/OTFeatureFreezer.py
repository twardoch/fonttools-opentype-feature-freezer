#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import opentype_feature_freezer
from opentype_feature_freezer.cli import main
from ezgooey.ez import *

version = opentype_feature_freezer.__version__

GUI_NAME = 'OTFeatureFreezer %s' % (version)
DESCRIPTION = 'Freeze some OpenType features into a font, see Help › %s Help.' % (GUI_NAME)


@ezgooey(
    advanced=True,
    auto_start=False,
    default_size=(800, 600),
    disable_progress_bar_animation=False,
    disable_stop_button=False,
    group_by_type=True,
    header_show_title=True,
    header_height=80,
    hide_progress_msg=False,
    optional_cols=1,
    program_description=DESCRIPTION,
    program_name=GUI_NAME,
    progress_expr=None,
    progress_regex=None,
    required_cols=1,
    richtext_controls=True,
    show_failure_modal=True,
    show_success_modal=False,
    suppress_gooey_flag=True,
    tabbed_groups=False,
    target=None,
    use_legacy_titles=True,
    menu=[{
        'name' : 'Help',
        'items': [{
            'type'       : 'AboutDialog',
            'menuTitle'  : 'About',
            'name'       : GUI_NAME,
            'description': 'Click the link for more info',
            'website'    : 'https://twardoch.github.io/fonttools-opentype-feature-freezer/',
            'license'    : 'Apache 2'
        }, {
            'type'     : 'Link',
            'menuTitle': '%s Help' % (GUI_NAME),
            'url'      : 'https://twardoch.github.io/fonttools-opentype-feature-freezer/'
        }]
    }]
)
def parseGuiOptions(args=None):
    parser = ArgumentParser(
        description=(
            'With %(prog)s you can "freeze" some OpenType features into a font. '
            'These features are then "on by default", even in apps that don\'t '
            'support OpenType features. Internally, the tool remaps the "cmap" '
            "table of the font by applying the specified GSUB features. Only "
            "single and alternate substitutions are supported."
        ),
        epilog=(
            "Examples: "
            "%(prog)s -f 'c2sc,smcp' -S -U SC OpenSans.ttf OpenSansSC.ttf "
            "%(prog)s -R 'Lato/Otal' Lato-Regular.ttf Otal-Regular.ttf"
        ),
    )

    parser.add_argument(
        "inpath",
        help="input .otf or .ttf font file",
        widget='FileChooser',
    )
    parser.add_argument(
        "-o", "--outpath",
        nargs="?",
        default=None,
        help="output .otf or .ttf font file (optional)",
        widget='FileSaver',
    )

    group_freezing = parser.add_argument_group("options to control feature freezing")
    group_freezing.add_argument(
        "-f",
        "--features",
        action="store",
        dest="features",
        type=str,
        default="",
        help="comma-separated list of OpenType feature tags, e.g. 'smcp,c2sc,onum'",
    )
    group_freezing.add_argument(
        "-s",
        "--script",
        action="store",
        dest="script",
        type=str,
        default=None,
        help="OpenType script tag, e.g. 'cyrl' (optional)",
    )
    group_freezing.add_argument(
        "-l",
        "--lang",
        action="store",
        dest="lang",
        type=str,
        default=None,
        help="OpenType language tag, e.g. 'SRB ' (optional)",
    )
    group_freezing.add_argument(
        "-z",
        "--zapnames",
        action="store_true",
        dest="zapnames",
        help="zap glyphnames from the font ('post' table version 3, .ttf only)",
    )

    group_renaming = parser.add_argument_group("options to control font renaming")
    group_renaming.add_argument(
        "-S",
        "--suffix",
        action="store_true",
        dest="suffix",
        help="add a suffix to the font family name (by default, the suffix will be constructed from the OpenType "
             "feature tags)",
    )
    group_renaming.add_argument(
        "-U",
        "--usesuffix",
        action="store",
        dest="usesuffix",
        default="",
        help="use a custom suffix when --suffix is provided",
    )
    group_renaming.add_argument(
        "-R",
        "--replacenames",
        action="store",
        dest="replacenames",
        default="",
        help="search for strings in the font naming tables and replace them, format is 'search1/replace1,"
             "search2/replace2,...'",
    )
    group_renaming.add_argument(
        "-i",
        "--info",
        action="store_true",
        dest="info",
        help="update font version string",
    )

    group_reporting = parser.add_argument_group("reporting options")
    group_reporting.add_argument(
        "-r",
        "--report",
        action="store_true",
        dest="report",
        help="report languages, scripts and features in font",
    )
    group_reporting.add_argument(
        "-n",
        "--names",
        action="store_true",
        dest="names",
        help="output names of remapped glyphs during processing",
    )
    group_reporting.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        const=True,
        default=True,
        dest="verbose",
        help="print additional information during processing",
    )

    return parser.parse_args(args)


if __name__ == "__main__":
    sys.exit(main(parser=parseGuiOptions))
