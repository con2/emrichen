import pytest

from emrichen import Template


def test_urlencode_str():
    assert Template.parse('!URLEncode "foo+bar"').enrich({}) == ['foo%2Bbar']


def test_urlencode_query():
    template = Template.parse(
        """
        !URLEncode
            query:
                foo: bar
"""
    )

    assert template.enrich({}) == ['foo=bar']


def test_urlencode_url():
    template = Template.parse(
        """
        !URLEncode
            url: "https://example.com/?foo=x"
            query:
                bar: xyzzy
"""
    )

    assert template.enrich({}) == ['https://example.com/?foo=x&bar=xyzzy']


def test_urlencode_enrich_str():
    assert (
        Template.parse(
            '''
!Defaults
bar: "foo+bar"
---
!URLEncode,Var bar
'''
        ).enrich({})
        == ['foo%2Bbar']
    )


def test_urlencode_enrich_url():
    template = Template.parse(
        """
!Defaults
bar: xyzzy
url: "https://example.com/?foo=x"
---
!URLEncode
    url: !Var url
    query:
        bar: !Var bar
"""
    )
    assert template.enrich({}) == ['https://example.com/?foo=x&bar=xyzzy']


def test_urlencode_enrich_query():
    template = Template.parse(
        """
!Defaults
bar: bar
---
!URLEncode
    query:
        foo: !Var bar
"""
    )
    assert template.enrich({}) == ['foo=bar']
