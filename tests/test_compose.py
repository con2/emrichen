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
