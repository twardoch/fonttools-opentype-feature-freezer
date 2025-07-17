# this_file: tests/test_version.py

import re
from opentype_feature_freezer import __version__


def test_version_format():
    """Test that version follows semantic versioning format."""
    # Should be either a proper semver or dev version
    semver_pattern = r"^\d+\.\d+\.\d+(?:[-+].+)?$"
    dev_pattern = r"^0\.0\.0\+unknown$"
    
    assert re.match(semver_pattern, __version__) or re.match(dev_pattern, __version__), \
        f"Version '{__version__}' does not follow expected format"


def test_version_is_string():
    """Test that version is a string."""
    assert isinstance(__version__, str)


def test_version_not_empty():
    """Test that version is not empty."""
    assert __version__
    assert len(__version__) > 0