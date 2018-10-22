from emrichen import Template


def test_op():
    template = Template.parse('''
!Op
  a: 1
  op: +
  b: 1
''', 'yaml')
    assert template.enrich({}) == [2]
