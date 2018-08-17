from emrichen import Context, Template


TEMPLATE = """
!Defaults
a:
  - 1
  - 2
b:
  - 3
  - 4
---
!Concat
  - !Var a
  - !Var b
  - - 5
    - 6
"""


def test_concat():
    assert Template.parse(TEMPLATE).enrich(Context()) == [[1, 2, 3, 4, 5, 6]]
