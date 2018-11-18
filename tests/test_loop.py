import pytest

from emrichen import Context, Template, Var
from emrichen.tags import Loop

LOOP_TEST_CONTEXT = {'domain_names': ['hernekeit.to', 'vii.na', 'teli.ne', 'johann.es']}


def test_loop(examples_dir):
    with open('{examples_dir}/loop.yml'.format(examples_dir=examples_dir), 'r') as inf:
        template = Template.parse(inf, 'yaml')
    ctx = Context(LOOP_TEST_CONTEXT)
    output = template.render(ctx)
    assert (
        output.strip()
        == '''
domains:
- apiVersion: v1
  kind: DomainName
  metadata:
    index: 0
    name: hernekeit.to
- apiVersion: v1
  kind: DomainName
  metadata:
    index: 1
    name: vii.na
- apiVersion: v1
  kind: DomainName
  metadata:
    index: 2
    name: teli.ne
- apiVersion: v1
  kind: DomainName
  metadata:
    index: 3
    name: johann.es
'''.strip()
    )


def test_loop_user_friendliness():
    template = Template([Loop({'over': 'domain_names', 'template': Var('item')})])
    ctx = Context(LOOP_TEST_CONTEXT)
    with pytest.raises(ValueError) as ei:
        output = template.render(ctx)
    assert 'did you mean' in str(ei.value)


def test_loop_index_start():
    template = Template.parse('''
!Loop
  over: [1, 2, 3]
  index_start: 5
  index_as: index
  template: !Var index
''')
    assert template.enrich({}) == [[5, 6, 7]]


def test_loop_over_dict():
    template = Template.parse('''
!Loop
  over:
    a: 5
    b: 6
  index_as: index
  template:
    item: !Var item
    index: !Var index
''')
    assert template.render({}).strip() == '''
- item: 5
  index: a
- item: 6
  index: b
'''.strip()


def test_no_index_start_with_dict():
    template = Template.parse('''
!Loop
  over:
    a: 5
  index_as: index
  index_start: 5
  template: 1
''')
    with pytest.raises(ValueError) as nope:
        template.render({})

    assert 'index_start with dict' in str(nope.value)
