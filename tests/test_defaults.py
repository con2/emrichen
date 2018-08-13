import os.path

import pytest

from emrichen import emrichen


with open(os.path.join(os.path.dirname(__file__), '..', 'examples', 'defaults', 'template.yml'), encoding='utf-8') as input_file:
    TEMPLATE = input_file.read()

BAD_TEMPLATE = """
this: !Defaults
  myvar: is not ok
"""


def test_defaults():
    output = emrichen(TEMPLATE, quux=6)
    assert 'bar' in output
    assert '6' in output


def test_bad_defaults():
    with pytest.raises(ValueError):
        emrichen(BAD_TEMPLATE)
