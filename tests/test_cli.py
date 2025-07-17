# this_file: tests/test_cli.py

import pytest
import sys
from unittest.mock import patch, MagicMock
from opentype_feature_freezer.cli import main, ArgumentParser


def test_argument_parser_creation():
    """Test that ArgumentParser can be created."""
    parser = ArgumentParser()
    assert parser is not None


def test_argument_parser_basic_args():
    """Test basic argument parsing."""
    parser = ArgumentParser()
    
    # Test with minimal required arguments
    args = parser.parse_args(['input.ttf'])
    assert args.inpath == 'input.ttf'
    assert args.outpath is None
    assert args.features is None
    assert args.script is None
    assert args.lang is None
    assert args.info is False
    assert args.names is False
    assert args.report is False
    assert args.suffix is False
    assert args.usesuffix is None
    assert args.verbose is False
    assert args.zapnames is False


def test_argument_parser_all_args():
    """Test parsing all arguments."""
    parser = ArgumentParser()
    
    args = parser.parse_args([
        '-f', 'smcp,c2sc',
        '-s', 'latn',
        '-l', 'ENG',
        '-S',
        '-U', 'SC',
        '-R', 'Old/New',
        '-v',
        '-i',
        '-n',
        '-z',
        'input.ttf',
        'output.ttf'
    ])
    
    assert args.inpath == 'input.ttf'
    assert args.outpath == 'output.ttf'
    assert args.features == 'smcp,c2sc'
    assert args.script == 'latn'
    assert args.lang == 'ENG'
    assert args.suffix is True
    assert args.usesuffix == 'SC'
    assert args.replacenames == ['Old/New']
    assert args.verbose is True
    assert args.info is True
    assert args.names is True
    assert args.zapnames is True


def test_main_with_help():
    """Test main function with help argument."""
    with patch('sys.argv', ['pyftfeatfreeze', '--help']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0


def test_main_with_version():
    """Test main function with version argument."""
    with patch('sys.argv', ['pyftfeatfreeze', '--version']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0


def test_main_with_missing_file():
    """Test main function with missing input file."""
    with patch('sys.argv', ['pyftfeatfreeze', 'nonexistent.ttf']):
        result = main()
        assert result == 1  # Should return error code


@patch('opentype_feature_freezer.RemapByOTL')
def test_main_with_valid_args(mock_remapper):
    """Test main function with valid arguments."""
    # Mock the RemapByOTL class
    mock_instance = MagicMock()
    mock_instance.success = True
    mock_remapper.return_value = mock_instance
    
    with patch('sys.argv', ['pyftfeatfreeze', '-f', 'smcp', 'test.ttf']):
        result = main()
        assert result == 0  # Should return success
        mock_remapper.assert_called_once()
        mock_instance.openFont.assert_called_once()


def test_main_callable():
    """Test that main function is callable."""
    assert callable(main)


def test_main_with_empty_args():
    """Test main function with no arguments."""
    with patch('sys.argv', ['pyftfeatfreeze']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 2  # argparse error code