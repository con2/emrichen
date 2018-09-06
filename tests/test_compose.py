import base64

import pytest

from emrichen import Context, Template
from emrichen.tags.compose import Compose

CONTEXT = {'thing': 'world'}


def test_compose_tag():
    comp = Compose({
        'tags': ['Base64', 'Format'],
        'value': 'hello {thing}',
    })
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
