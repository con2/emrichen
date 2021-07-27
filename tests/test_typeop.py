import pytest

from emrichen import Context, Template
from emrichen.void import Void


@pytest.mark.parametrize(
    'tag, val, result',
    [
        ('IsBoolean', 0, False),
        ('IsBoolean', False, True),
        ('IsBoolean', True, True),
        ('IsDict', [], False),
        ('IsDict', {}, True),
        ('IsInteger', 8, True),
        ('IsInteger', 8.2, False),
        ('IsInteger', False, False),  # Ylläri!
        ('IsInteger', True, False),  # Ylläri!
        ('IsList', 8, False),
        ('IsList', [], True),
        ('IsNone', '', False),
        ('IsNone', None, True),
        ('IsNone', Void, True),
        ('IsNumber', 8, True),
        ('IsNumber', 8.2, True),
        ('IsNumber', False, False),  # Ylläri!
        ('IsNumber', True, False),  # Ylläri!
        ('IsString', 'yes', True),
        ('IsString', 8, False),
        ('IsString', Void, False),
    ],
)
def test_typeop(tag, val, result):
    resolved = Template.parse(f"!{tag},Lookup 'a'").enrich(Context({'a': val}))[0]
    assert resolved == result, f'{tag}({val!r}) returned {resolved}, expected {result}'
