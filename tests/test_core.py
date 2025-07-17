# this_file: tests/test_core.py

import pytest
import tempfile
from pathlib import Path
from types import SimpleNamespace
from opentype_feature_freezer import RemapByOTL
import fontTools.ttLib


def test_remapbyotl_init():
    """Test RemapByOTL initialization."""
    options = SimpleNamespace()
    options.inpath = "test_input.ttf"
    options.outpath = "test_output.ttf"
    options.features = "smcp,c2sc"
    options.script = None
    options.lang = None
    options.info = False
    options.names = False
    options.report = False
    options.replacenames = []
    options.suffix = False
    options.usesuffix = None
    options.verbose = False
    options.zapnames = False
    
    remapper = RemapByOTL(options)
    
    assert remapper.inpath == "test_input.ttf"
    assert remapper.outpath == "test_output.ttf"
    assert remapper.options == options
    assert remapper.success is True
    assert remapper.substitution_mapping == {}


def test_remapbyotl_default_outpath():
    """Test RemapByOTL with default output path."""
    options = SimpleNamespace()
    options.inpath = "test_input.ttf"
    options.outpath = None
    options.features = "smcp"
    options.script = None
    options.lang = None
    options.info = False
    options.names = False
    options.report = False
    options.replacenames = []
    options.suffix = False
    options.usesuffix = None
    options.verbose = False
    options.zapnames = False
    
    remapper = RemapByOTL(options)
    
    assert remapper.outpath == "test_input.ttf.featfreeze.otf"


def test_open_nonexistent_font():
    """Test opening a non-existent font file."""
    options = SimpleNamespace()
    options.inpath = "nonexistent.ttf"
    options.outpath = None
    options.features = "smcp"
    options.script = None
    options.lang = None
    options.info = False
    options.names = False
    options.report = False
    options.replacenames = []
    options.suffix = False
    options.usesuffix = None
    options.verbose = False
    options.zapnames = False
    
    remapper = RemapByOTL(options)
    remapper.openFont()
    
    assert remapper.success is False
    assert remapper.ttx is None


def test_open_valid_font(tmp_path, shared_datadir):
    """Test opening a valid font file."""
    # Create a temporary font file
    font = fontTools.ttLib.TTFont()
    font.importXML(shared_datadir / "OpenSans-Bold.subset.ttx")
    font_path = tmp_path / "Test.ttf"
    font.save(font_path)
    
    options = SimpleNamespace()
    options.inpath = str(font_path)
    options.outpath = None
    options.features = "smcp"
    options.script = None
    options.lang = None
    options.info = False
    options.names = False
    options.report = False
    options.replacenames = []
    options.suffix = False
    options.usesuffix = None
    options.verbose = False
    options.zapnames = False
    
    remapper = RemapByOTL(options)
    remapper.openFont()
    
    assert remapper.success is True
    assert remapper.ttx is not None
    assert isinstance(remapper.ttx, fontTools.ttLib.TTFont)