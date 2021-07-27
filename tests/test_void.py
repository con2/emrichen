import json

from emrichen import Template, emrichen

TEMPLATE = Template.parse(
    """
Smile: !Void
Sweet: !Void
Sister: !Void
Sadistic: !Void
Surprise: true
Service: !Void
""",
    'yaml',
)


def test_void_yaml():
    assert TEMPLATE.render({}, 'yaml').strip() == 'Surprise: true'


def test_void_json():
    assert json.loads(TEMPLATE.render({}, 'json')) == {"Surprise": True}


def test_void_top_level():
    assert emrichen('!Void\n---!Void\n---\na: 5').strip() == 'a: 5'
