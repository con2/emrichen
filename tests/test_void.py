import json

from emrichen import Template

template = Template.parse("""
Smile: !Void
Sweet: !Void
Sister: !Void
Sadistic: !Void
Surprise: true
Service: !Void
""", 'yaml')


def test_void_yaml():
    assert template.render({}, 'yaml').strip() == 'Surprise: true'

def test_void_json():
    assert json.loads(template.render({}, 'json')) == [{"Surprise": True}]
