import pytest

from emrichen import emrichen


TEMPLATE = """
---
foo:
  bar:
    quux: !Error "Everything went better than exception"
"""


def test_error():
    with pytest.raises(ValueError):
        emrichen(TEMPLATE)
