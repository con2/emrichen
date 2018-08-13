from emrichen import Template


def test_if():
    template = Template.parse('''
!If
  a: !Lookup chance
  op: gt
  b: .5
  then: !Format "This is {person.name}, hello"
  else: No chance
''', 'yaml')
    base = {'person': {'name': 'dog'}}
    assert template.enrich(dict(base, chance=.99))[0] == 'This is dog, hello'
    assert template.enrich(dict(base, chance=.5))[0] == 'No chance'


def test_filter_list():
    template = Template.parse('''
!Filter
  over:
  - valid
  - hello
  - 0
  - SSEJ
  - false
  - null
  test:
    a: !Lookup item
''', 'yaml')
    assert template.enrich({})[0] == ['valid', 'hello', 'SSEJ']


def test_filter_dict():
    template = Template.parse('''
!Filter
  over:
    'yes': true
    no: 0
    nope: false
    oui: 1
''', 'yaml')
    assert template.enrich({})[0] == {'oui': 1, 'yes': True}


def test_if_void():
    template = Template.parse('''
result: !If
  a: !Lookup chance
  op: gt
  b: .5
  then: !Format "This is {person.name}, hello"
''', 'yaml')
    base = {'person': {'name': 'dog'}}
    assert template.render(dict(base, chance=.99)).strip() == 'result: This is dog, hello'
    assert template.render(dict(base, chance=.5)).strip() == '{}'
