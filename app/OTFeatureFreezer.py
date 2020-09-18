#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from opentype_feature_freezer.cli import *
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
    tabbed_groups=True,
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
            'menuTitle': '%s Documentation' % (GUI_NAME),
            'url'      : 'https://twardoch.github.io/fonttools-opentype-feature-freezer/'
        }]
    }]
)
def gui():
    main()

gui()