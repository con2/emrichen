import pytest

from emrichen import Context, Template, Var
from emrichen.tags import Loop

LOOP_TEST_CONTEXT = {'domain_names': ['hernekeit.to', 'vii.na', 'teli.ne', 'johann.es']}


def test_loop(examples_dir):
    with open(f'{examples_dir}/loop.yml', 'r') as inf:
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
