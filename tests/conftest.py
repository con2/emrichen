import os

import pytest


@pytest.fixture
def examples_dir():
    return os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'examples'))
