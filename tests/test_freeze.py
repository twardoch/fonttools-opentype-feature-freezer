import logging
import tempfile

import fontTools.ttLib

import opentype_feature_freezer.cli


def test_freeze(tmp_path, shared_datadir):
    font = fontTools.ttLib.TTFont()
    font.importXML(shared_datadir / "OpenSans-Bold.subset.ttx")
    font_path = tmp_path / "Test.ttf"
    font.save(font_path)

    opentype_feature_freezer.cli.main(
        ["-v", "-f", "c2sc,onum,smcp", "-S", "-U", "SC", "--names", str(font_path)]
    )

    font_processed = fontTools.ttLib.TTFont(
        tmp_path / (font_path.name + ".featfreeze.otf")
    )
    cmap = font_processed.getBestCmap()
    assert cmap[0x30] == "zero.os"
    assert cmap[0x31] == "one.os"
    assert cmap[0x32] == "two.os"
    assert cmap[0x33] == "three.os"
    assert cmap[0x34] == "four.os"
    assert cmap[0x35] == "five.os"
    assert cmap[0x36] == "six.os"
    assert cmap[0x37] == "seven.os"
    assert cmap[0x38] == "eight.os"
    assert cmap[0x39] == "nine.os"


def test_report(tmp_path, shared_datadir, capsys):
    font = fontTools.ttLib.TTFont()
    font.importXML(shared_datadir / "OpenSans-Bold.subset.ttx")
    font_path = tmp_path / "Test.ttf"
    font.save(font_path)

    opentype_feature_freezer.cli.main(
        ["-v", "-f", "c2sc,onum,smcp", "-S", "-U", "SC", "--report", str(font_path)]
    )

    captured = capsys.readouterr()
    assert (
        captured.out
        == """# Scripts and languages:
-s 'latn'
# Features:
-f lnum,onum,pnum,tnum
"""
    )


def test_cant_open():
    with tempfile.NamedTemporaryFile() as f:
        assert (
            opentype_feature_freezer.cli.main(
                ["-v", "-f", "c2sc,onum,smcp", "-S", "-U", "SC", f.name]
            )
            == 1
        )


def test_warn_substituting_glyphs_without_unicode(tmp_path, shared_datadir, caplog):
    font = fontTools.ttLib.TTFont()
    font.importXML(shared_datadir / "SubGlyphsWithoutUnicode.ttx")
    font_path = tmp_path / "Test.ttf"
    font.save(font_path)

    opentype_feature_freezer.cli.main(["-v", "-f", "ss01", "--names", str(font_path)])
    assert any(
        record.levelno == logging.WARNING
        and "neither has a Unicode value" in record.message
        for record in caplog.records
    )

    font_processed = fontTools.ttLib.TTFont(
        tmp_path / (font_path.name + ".featfreeze.otf")
    )
    cmap = font_processed.getBestCmap()
    assert cmap == {0x61: "a.alt1"}  # Takes the first alternate
