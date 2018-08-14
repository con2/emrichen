from emrichen import emrichen


TEMPLATE = """
!Defaults
foo: bar
---
yep: !Exists foo
nope: !Exists quux
"""


def test_exists():
    assert emrichen(TEMPLATE).strip() == 'nope: false\nyep: true'
