import os.path

import pytest

from emrichen import Template


BASE_DIR = os.path.realpath(os.path.dirname(__file__))


def test_include_good():
    filename = os.path.join(BASE_DIR, 'test_include_good.in.yml')
    template = Template.parse('!Include includes/good.in.yml', filename=filename)
    assert template.enrich({}) == [{'foo': 5}]


def test_include_chained():
    filename = os.path.join(BASE_DIR, 'test_include_chained.in.yml')
    template = Template.parse('!Include includes/chained.in.yml', filename=filename)
    assert template.enrich({}) == [{'bar': {'foo': 5}, 'bar2': {'foo': 5}}]


def test_include_multi_void():
    filename = os.path.join(BASE_DIR, 'test_include_multi_void.in.yml')
    template = Template.parse('!Include includes/multi_void.in.yml', filename=filename)
    assert template.enrich({}) == [{'foo': 5}]


def test_include_void():
    filename = os.path.join(BASE_DIR, 'test_include_void.in.yml')
    template = Template.parse('!Include includes/void.in.yml', filename=filename)
    assert template.enrich({}) == []


def test_include_empty():
    filename = os.path.join(BASE_DIR, 'test_include_empty.in.yml')
    template = Template.parse('!Include includes/empty.in.yml', filename=filename)
    assert template.enrich({}) == []


def test_include_multi():
    filename = os.path.join(BASE_DIR, 'test_include_multi.in.yml')
    template = Template.parse('!Include includes/multi.in.yml', filename=filename)

    with pytest.raises(ValueError) as err:
        template.enrich({})

    assert 'single-document' in str(err.value)


def test_mixed_format():
    filename = os.path.join(BASE_DIR, 'test_include_mixed_format.in.yml')
    template = Template.parse('!Include includes/chained.in.json', filename=filename)
    assert template.enrich({}) == [{'bar': {'foo': 5}}]


def test_include_defaults():
    filename = os.path.join(BASE_DIR, 'test_include_defaults.in.yml')
    template = Template.parse('''
!Include includes/defaults.in.yml
---
foo: !Var foo
''', filename=filename)
    assert template.enrich({}) == [{'foo': 5}]


def test_consecutive_include_at_top_level():
    filename = os.path.join(BASE_DIR, 'test_consecutive_include_at_top_level.in.yml')
    template = Template.parse('''
!Include includes/good.in.yml
---
!Include includes/good.in.yml
''', filename=filename)
    assert template.enrich({}) == [{'foo': 5}, {'foo': 5}]


def test_include_chained_defaults():
    filename = os.path.join(BASE_DIR, 'test_include_chained_defaults.in.yml')
    template = Template.parse('''
!Include includes/chained_defaults.in.yml
---
foo: !Var foo
''', filename=filename)
    assert template.enrich({}) == [{'foo': 5}]


def test_include_text_and_base64():
    filename = os.path.join(BASE_DIR, 'test_include_text_and_base64.in.yml')
    template = Template.parse('''
apiVersion: v1
kind: ConfigMap
metadata:
  name: config
data:
  image.png.b64: !IncludeBase64 includes/intense50.png
  config.toml: !IncludeText includes/data.toml
''', filename=filename)
    data = template.enrich({})[0]['data']
    assert data['image.png.b64'].startswith('iVBORw0KGgoAAAANSUhEUgA')
    assert data['config.toml'].startswith('[database]\nserver =')


def test_include_glob():
    filename = os.path.join(BASE_DIR, 'test_include_glob.yml')
    template = Template.parse('!IncludeGlob ["includes/globhierarchy/**", "includes/multi*yml"]', filename=filename)
    greeting = "Hello"
    salutation = "Fare thee well"
    result = template.enrich({"greeting": greeting, "salutation": salutation})[0]
    assert [dict(od.items()) for od in result] == [
        # 01.yml's documents
        {'first': greeting},
        {'second': True},
        # z.yml's document
        {'middle': 42},
        # 99.yml's documents
        {'penultimate': True},
        {'last': salutation},
        # multi.in.yml
        {'foo': 5},
        {'bar': 6},
        # multi_void.in.yml (two voids elided)
        {'foo': 5},
    ]
