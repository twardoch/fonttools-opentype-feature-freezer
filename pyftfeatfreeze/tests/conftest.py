from pathlib import Path

import pytest


@pytest.fixture
def shared_datadir() -> Path:
    return Path(__file__).parent / "data"
