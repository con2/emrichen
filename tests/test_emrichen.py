from emrichen import emrichen


TEMPLATE = """
---
foo: bar
quux:
  xyzzy: !Var kitten
"""

VARIABLES = """
kitten: meow
"""

EXPECTED = """foo: bar
quux:
  xyzzy: meow
"""


def test_emrichen():
    output = emrichen(TEMPLATE, VARIABLES)
    assert output == EXPECTED
