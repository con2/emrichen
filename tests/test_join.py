from emrichen import emrichen


def test_simple_join():
    assert emrichen('foo: !Join [1, 2, 3]').strip() == 'foo: 1 2 3'


def test_join_with_separator():
    assert (
        emrichen(
            '''
!Defaults
flavors:
    - pea soup
    - hard liquor
    - manifold
    - John
---
foo: !Join
    items: !Var flavors
    separator: ' -> '
'''
        ).strip()
        == 'foo: pea soup -> hard liquor -> manifold -> John'
    )
