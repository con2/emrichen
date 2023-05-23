import pytest

from emrichen import Context, Template

LOOKUP_TEST_CONTEXT = {
    'people': [
        {'first_name': 'Minnie', 'last_name': 'Duck'},
        {'first_name': 'Popuko', 'last_name': 'Pipimi'},
    ]
}


def test_lookup_all():
    template = Template.parse(
        '''
first_names: !LookupAll people[*].first_name
last_names: !LookupAll people[*].last_name
''',
        'yaml',
    )
    ctx = Context(LOOKUP_TEST_CONTEXT)
    output = template.render(ctx)
    assert (
        output.strip()
        == '''
first_names:
- Minnie
- Popuko
last_names:
- Duck
- Pipimi
'''.strip()
    )


def test_lookup():
    template = Template.parse(
        '''
people:
  !Loop
    over: !Var people
    as: person
    template:
      - !Lookup person.last_name
      - !Lookup person.first_name
''',
        'yaml',
    )
    ctx = Context(LOOKUP_TEST_CONTEXT)
    output = template.render(ctx)
    assert (
        output.strip()
        == '''
people:
- - Duck
  - Minnie
- - Pipimi
  - Popuko
'''.strip()
    )


def test_lookup_no_match():
    template = Template.parse('''!Lookup people..nep''', 'yaml')
    with pytest.raises(KeyError) as ei:
        ctx = Context(LOOKUP_TEST_CONTEXT)
        template.render(ctx)
    assert 'no matches for' in str(ei.value)


def test_late_enrich():
    template = Template.parse(
        '''
!Defaults
x:
  y: 5
z: !Var x
---
workie: !Lookup x.y
no_workie: !Lookup z.y
''',
        format='yaml',
    )
    assert template.enrich({}) == [{'workie': 5, 'no_workie': 5}]


def test_lookup_enrich():
    """
    Lookup should enrich whatever it returns.
    """
    template = Template.parse(
        '''
!Defaults
x: [5]
y: !Var x
z: !Lookup y
---
should_contain_5: !Loop
  over: !Var z
  as: item
  template: !Var item
'''
    )
    assert template.enrich({}) == [{'should_contain_5': [5]}]


@pytest.mark.xfail
def test_recursive_data_structure():
    template = Template.parse('''
!Defaults
x:
    y: 5
    x: !Var x
---
five: !Lookup x.y
also_five: !Lookup x.x.x.x.x.y
''')
    assert template.enrich({}) == [{'five': 5, 'also_five': 5}]
