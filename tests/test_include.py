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
