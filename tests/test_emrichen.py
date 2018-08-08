from emrichen import emrichen


TEMPLATE = """
---
foo: bar
quux:
  xyzzy: !Var kitten
  klik: !Format "{klak} kluk"
"""

VARIABLES = """
kitten: meow
klak: klok
"""

EXPECTED = """foo: bar
quux:
  klik: klok kluk
  xyzzy: meow
"""


def test_emrichen():
    output = emrichen(TEMPLATE, VARIABLES)
    assert output == EXPECTED
