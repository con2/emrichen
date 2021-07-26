from emrichen import Template


def test_if():
    template = Template.parse(
        '''
!If
  test: !Op
    a: !Lookup chance
    op: gt
    b: .5
  then: !Format "This is {person.name}, hello"
  else: No chance
''',
        'yaml',
    )
    base = {'person': {'name': 'dog'}}
    assert template.enrich(dict(base, chance=0.99))[0] == 'This is dog, hello'
    assert template.enrich(dict(base, chance=0.5))[0] == 'No chance'


def test_filter_list():
    template = Template.parse(
        '''
!Filter
  over:
  - valid
  - hello
  - 0
  - SSEJ
  - false
  - null
''',
        'yaml',
    )
    assert template.enrich({})[0] == ['valid', 'hello', 'SSEJ']


def test_filter_dict():
    template = Template.parse(
        '''
!Filter
  as: i
  test: !Not,Var i
  over:
    'yes': true
    no: 0
    nope: false
    oui: 1
''',
        'yaml',
    )
    assert template.enrich({})[0] == {False: 0, 'nope': False}


def test_filter_op():
    template = Template.parse(
        '''
!Filter
  test: !Op
    a: !Var item
    op: gt
    b: 4
  over: [1, 7, 2, 5]
'''
    )
    assert template.enrich({}) == [[7, 5]]


def test_if_void():
    template = Template.parse(
        '''
result: !If
  test: !Op
    a: !Lookup chance
    op: gt
    b: .5
  then: !Format "This is {person.name}, hello"
''',
        'yaml',
    )
    base = {'person': {'name': 'dog'}}
    assert template.render(dict(base, chance=0.99)).strip() == 'result: This is dog, hello'
    assert template.render(dict(base, chance=0.5)).strip() == '{}'
