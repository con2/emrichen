from emrichen import emrichen


TEMPLATE = """
---
foo: !With
  vars:
    foo: 5
    bar: !Var foo
  template: !Var bar
"""


def test_with():
    assert emrichen(TEMPLATE).strip() == "foo: 5"
