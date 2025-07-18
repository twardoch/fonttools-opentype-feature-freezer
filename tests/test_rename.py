from argparse import Namespace

import fontTools.ttLib

import opentype_feature_freezer


def test_rename_ttf(shared_datadir):
    font = fontTools.ttLib.TTFont()
    font.importXML(shared_datadir / "Empty_TTF.ttx")

    # Using Namespace and adding 'suffix' attribute
    remapper_options = Namespace(
        inpath="None",
        outpath=None,
        # rename=True, # This attribute is not used by RemapByOTL directly
        suffix=True,  # Explicitly add suffix based on command line options
        usesuffix="Asdf",
        replacenames="Test/Rest Dest",
        info=True,
        features="smcp,c2sc,onum",
        # Add other attributes that parseOptions would create, with defaults
        script=None,
        lang=None,
        zapnames=False,
        report=False,
        names=False,  # For self.options.names in applySubstitutions
        verbose=False,
    )
    remapper = opentype_feature_freezer.RemapByOTL(remapper_options)
    remapper.ttx = font
    remapper.renameFont()

    font_name = font["name"]
    assert font_name.getName(0, 3, 1, 1033).toStr() == "Test Corp"
    assert font_name.getName(1, 3, 1, 1033).toStr() == "Rest Dest Asdf"
    assert font_name.getName(2, 3, 1, 1033).toStr() == "Regular"
    assert (
        font_name.getName(3, 3, 1, 1033).toStr()
        == "1.001;NONE;Test-Regular;featfreeze:smcp,c2sc,onum"
    )
    assert font_name.getName(4, 3, 1, 1033).toStr() == "Rest Dest Asdf Regular"
    assert (
        font_name.getName(5, 3, 1, 1033).toStr()
        == "Version 1.001; featfreeze: smcp,c2sc,onum"
    )
    assert font_name.getName(6, 3, 1, 1033).toStr() == "RestDestAsdf-Regular"


def test_rename_ttf_no_replace(shared_datadir):
    font = fontTools.ttLib.TTFont()
    font.importXML(shared_datadir / "Empty_TTF.ttx")

    remapper_options = Namespace(
        inpath="None",
        outpath=None,
        suffix=True,  # Explicitly add suffix
        usesuffix="Asdf",
        replacenames="",
        info=True,
        features="smcp,c2sc,onum",
        script=None,
        lang=None,
        zapnames=False,
        report=False,
        names=False,
        verbose=False,
    )
    remapper = opentype_feature_freezer.RemapByOTL(remapper_options)
    remapper.ttx = font
    remapper.renameFont()

    font_name = font["name"]
    assert font_name.getName(0, 3, 1, 1033).toStr() == "Test Corp"
    assert font_name.getName(1, 3, 1, 1033).toStr() == "Test Asdf"
    assert font_name.getName(2, 3, 1, 1033).toStr() == "Regular"
    assert (
        font_name.getName(3, 3, 1, 1033).toStr()
        == "1.001;NONE;Test-Regular;featfreeze:smcp,c2sc,onum"
    )
    assert font_name.getName(4, 3, 1, 1033).toStr() == "Test Asdf Regular"
    assert (
        font_name.getName(5, 3, 1, 1033).toStr()
        == "Version 1.001; featfreeze: smcp,c2sc,onum"
    )
    assert font_name.getName(6, 3, 1, 1033).toStr() == "TestAsdf-Regular"


def test_rename_ttf_autosuffix(shared_datadir):
    font = fontTools.ttLib.TTFont()
    font.importXML(shared_datadir / "Empty_TTF.ttx")

    remapper_options = Namespace(
        inpath="None",
        outpath=None,
        suffix=True,  # Suffix is True for autosuffix generation
        usesuffix="",  # Empty usesuffix means auto-generate from features
        replacenames="",
        info=True,
        features="smcp,c2sc,onum",
        script=None,
        lang=None,
        zapnames=False,
        report=False,
        names=False,
        verbose=False,
    )
    remapper = opentype_feature_freezer.RemapByOTL(remapper_options)
    remapper.ttx = font
    remapper.filterByFeatures = ["smcp", "c2sc", "onum"]
    remapper.renameFont()

    font_name = font["name"]
    assert font_name.getName(0, 3, 1, 1033).toStr() == "Test Corp"
    assert font_name.getName(1, 3, 1, 1033).toStr() == "Test c2sc onum smcp"
    assert font_name.getName(2, 3, 1, 1033).toStr() == "Regular"
    assert (
        font_name.getName(3, 3, 1, 1033).toStr()
        == "1.001;NONE;Test-Regular;featfreeze:smcp,c2sc,onum"
    )
    assert font_name.getName(4, 3, 1, 1033).toStr() == "Test c2sc onum smcp Regular"
    assert (
        font_name.getName(5, 3, 1, 1033).toStr()
        == "Version 1.001; featfreeze: smcp,c2sc,onum"
    )
    assert font_name.getName(6, 3, 1, 1033).toStr() == "Testc2sconumsmcp-Regular"


def test_rename_ttf_with_nameid16(shared_datadir):
    font = fontTools.ttLib.TTFont()
    font.importXML(shared_datadir / "EmptyNameID16_TTF.ttx")

    remapper_options = Namespace(
        inpath="None",
        outpath=None,
        suffix=True,
        usesuffix="Asdf",
        replacenames="Test/Rest Dest",
        info=True,
        features="smcp,c2sc,onum",
        script=None,
        lang=None,
        zapnames=False,
        report=False,
        names=False,
        verbose=False,
    )
    remapper = opentype_feature_freezer.RemapByOTL(remapper_options)
    remapper.ttx = font
    remapper.renameFont()

    font_name = font["name"]
    assert font_name.getName(0, 3, 1, 1033).toStr() == "Test Corp"
    assert font_name.getName(1, 3, 1, 1033).toStr() == "Rest Dest Asdf zxcv"
    assert font_name.getName(2, 3, 1, 1033).toStr() == "Regular"
    assert (
        font_name.getName(3, 3, 1, 1033).toStr()
        == "1.001;NONE;Test-zxcv;featfreeze:smcp,c2sc,onum"
    )
    assert font_name.getName(4, 3, 1, 1033).toStr() == "Rest Dest Asdf zxcv"
    assert (
        font_name.getName(5, 3, 1, 1033).toStr()
        == "Version 1.001; featfreeze: smcp,c2sc,onum"
    )
    assert font_name.getName(6, 3, 1, 1033).toStr() == "RestDestAsdf-zxcv"
    assert font_name.getName(16, 3, 1, 1033).toStr() == "Rest Dest Asdf"
    assert font_name.getName(17, 3, 1, 1033).toStr() == "zxcv"


def test_rename_otf(shared_datadir):
    font = fontTools.ttLib.TTFont()
    font.importXML(shared_datadir / "Empty_OTF.ttx")

    remapper_options = Namespace(
        inpath="None",
        outpath=None,
        suffix=True,
        usesuffix="Asdf",
        replacenames="Test/Rest Test",
        info=True,
        features="smcp,c2sc,onum",
        script=None,
        lang=None,
        zapnames=False,
        report=False,
        names=False,
        verbose=False,
    )
    remapper = opentype_feature_freezer.RemapByOTL(remapper_options)
    remapper.ttx = font
    remapper.renameFont()

    font_name = font["name"]
    assert font_name.getName(0, 3, 1, 1033).toStr() == "Test Corp"
    assert font_name.getName(1, 3, 1, 1033).toStr() == "Rest Test Asdf"
    assert font_name.getName(2, 3, 1, 1033).toStr() == "Regular"
    assert (
        font_name.getName(3, 3, 1, 1033).toStr()
        == "1.001;NONE;Test-Regular;featfreeze:smcp,c2sc,onum"
    )
    assert font_name.getName(4, 3, 1, 1033).toStr() == "Rest Test Asdf Regular"
    assert (
        font_name.getName(5, 3, 1, 1033).toStr()
        == "Version 1.001; featfreeze: smcp,c2sc,onum"
    )
    assert font_name.getName(6, 3, 1, 1033).toStr() == "RestTestAsdf-Regular"

    font_cff_dict = font["CFF "].cff[0].rawDict
    assert font["CFF "].cff[0].Copyright == b"Test Corp"
    assert "FontName" not in font_cff_dict
    assert font_cff_dict["FullName"] == b"Rest Test Asdf Regular"
    assert font_cff_dict["FamilyName"] == b"Rest Test Asdf"


def test_rename_otf_with_nameid16(shared_datadir):
    font = fontTools.ttLib.TTFont()
    font.importXML(shared_datadir / "EmptyNameID16_OTF.ttx")

    remapper_options = Namespace(
        inpath="None",
        outpath=None,
        suffix=True,
        usesuffix="Asdf",
        replacenames="Test/Rest Test",
        info=True,
        features="smcp,c2sc,onum",
        script=None,
        lang=None,
        zapnames=False,
        report=False,
        names=False,
        verbose=False,
    )
    remapper = opentype_feature_freezer.RemapByOTL(remapper_options)
    remapper.ttx = font
    remapper.renameFont()

    font_name = font["name"]
    assert font_name.getName(1, 3, 1, 1033).toStr() == "Rest Test Asdf zxcv"
    assert font_name.getName(2, 3, 1, 1033).toStr() == "Regular"
    assert (
        font_name.getName(3, 3, 1, 1033).toStr()
        == "1.001;NONE;Test-zxcv;featfreeze:smcp,c2sc,onum"
    )
    assert font_name.getName(4, 3, 1, 1033).toStr() == "Rest Test Asdf zxcv"
    assert (
        font_name.getName(5, 3, 1, 1033).toStr()
        == "Version 1.001; featfreeze: smcp,c2sc,onum"
    )
    assert font_name.getName(6, 3, 1, 1033).toStr() == "RestTestAsdf-zxcv"
    assert font_name.getName(16, 3, 1, 1033).toStr() == "Rest Test Asdf"
    assert font_name.getName(17, 3, 1, 1033).toStr() == "zxcv"

    font_cff_dict = font["CFF "].cff[0].rawDict
    assert font["CFF "].cff[0].Copyright == b"Test Corp"
    assert "FontName" not in font_cff_dict
    assert font_cff_dict["FullName"] == b"Rest Test Asdf zxcv"
    assert font_cff_dict["FamilyName"] == b"Rest Test Asdf"
