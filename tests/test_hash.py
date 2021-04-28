import pytest

from emrichen import Template

HASHES = {
    'MD5': '8b1a9953c4611296a827abf8c47804d7',
    'SHA1': 'f7ff9e8b7bb2e09b70935a5d785e0cc5d9d0abf0',
    'SHA256': '185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969',
}


@pytest.mark.parametrize('h', sorted(HASHES.items()), ids=sorted(HASHES))
def test_hash(h):
    algo, expected = h
    assert Template.parse(f'!{algo} "Hello"').enrich({}) == [expected]
