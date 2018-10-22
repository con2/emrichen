from emrichen import Template


def test_op():
    template = Template.parse('''
!Op
  a: 1
  op: +
  b: 1
''', 'yaml')
    assert template.enrich({}) == [2]


def test_op_list():
    template = Template.parse('!Op [1, +, 1]')
    assert template.enrich({}) == [2]
