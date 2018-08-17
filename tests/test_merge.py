from emrichen import Context, Template


TEMPLATE = """
!Defaults
a:
  foo: 5
  bar: 6
---
!Merge
  - !Var a
  - bar: 7
"""


def test_merge():
    assert Template.parse(TEMPLATE).enrich(Context()) == [{"foo": 5, "bar": 7}]
