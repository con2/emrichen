import pytest

from emrichen import Template, Context
from emrichen.void import Void


@pytest.mark.parametrize(
    'tag, val, result',
    [
        ('ToBoolean', 0, False),
        # ('ToBoolean', "false", False),
        ('ToBoolean', "TRUE", True),
        ('ToInteger', "8", 8),
        ('ToInteger', {"value": "0644", "radix": 8}, 420),
        ('ToFloat', "8.2", 8.2),
        ('ToFloat', 8, 8.0),
        ('ToFloat', True, 1.0),
        ('ToString', True, "True"),  # TODO too pythonic? should we return lowercase instead?
        ('ToString', 8, "8"),
        # ('ToString', {'a': 5, 'b': 6}, "{'a': 5, 'b': 6}"),  # TODO OrderedDict([('a', 5), ('b', 6)])
    ],
)
def test_typeop(tag, val, result):
    resolved = Template.parse(f"!{tag},Lookup 'a'").enrich(Context({'a': val}))[0]
    assert resolved == result, f'{tag}({val!r}) returned {resolved}, expected {result}'

    # type equivalence instead of isinstance is intended: want strict conformance
    assert type(resolved) == type(
        result
    ), f'{tag}({val!r}) returned type {type(resolved)}, expected {type(result)}'
