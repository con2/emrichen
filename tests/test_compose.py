import base64

import pytest

from emrichen import Context, Template
from emrichen.tags.compose import Compose

CONTEXT = {'thing': 'world'}


def test_compose_tag():
    comp = Compose(
        {
            'tags': ['Base64', 'Format'],
            'value': 'hello {thing}',
        }
    )
    ctx = Context(CONTEXT)
    output = comp.enrich(ctx)
    assert base64.b64decode(output).decode() == 'hello world'


@pytest.mark.parametrize('format', ('json', 'yaml'))
def test_compose_syntax(format):
    source = {
        'yaml': '!Base64,Format "hello {thing}"',
        'json': '{"!Base64,Format": "hello {thing}"}',
    }
    template = Template.parse(source[format], format)
    ctx = Context(CONTEXT)
    output = template.enrich(ctx)[0]
    assert base64.b64decode(output).decode() == 'hello world'


def test_compose_context():
    """
    There was a bug in handling of Context in Compose that would cause Loop within Compose
    to not propagate `as`, `index_as` etc within `template`. Prior to fixing of that bug,
    this test would `KeyError: item`.
    """
    template = Template.parse(
        '''
!Concat,Loop
  over:
    - [1, 2, 3]
    - [4, 5, 6]
  as: item
  template: !Var item
'''
    )
    assert template.enrich({}) == [[1, 2, 3, 4, 5, 6]]


def test_compose_context_json():
    template = Template.parse(
        '''
{
    "!Concat": {
        "!Loop": {
            "over": [
                [1, 2, 3],
                [4, 5, 6]
            ],
            "as": "item",
            "template": {
                "!Var": "item"
            }
        }
    }
}
''',
        'json',
    )
    assert template.enrich({}) == [[1, 2, 3, 4, 5, 6]]
