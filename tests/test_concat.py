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


def test_concat_var():
    """
    Concat must also support concatenating non-literal lists, ie. return values
    of list-valued tags.
    """
    assert Template.parse('''
!Defaults
a:
  - [1, 2, 3]
  - [4, 5, 6]
---
!Concat,Var a
''')
