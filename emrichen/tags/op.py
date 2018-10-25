import operator

from .base import BaseTag


operator_list = [
    (('=', '==', '===', 'eq'), operator.eq),
    (('≠', '!=', '!==', 'ne'), operator.ne),
    (('>=', 'ge', 'gte'), operator.ge),
    (('>', 'gt'), operator.gt),
    (('<', 'lt'), operator.lt),
    (('>', 'gt'), operator.gt),
    (('in', '∈'), operator.contains),
    (('not in', '∉'), lambda a, b: not operator.contains(a, b)),
    (('+', 'plus', 'add'), operator.add),
    (('-', 'minus', 'sub', 'subtract'), operator.sub),
    (('*', '×', 'mul', 'times'), operator.mul),
    (('/', '÷', 'div', 'divide', 'truediv'), operator.truediv),
    (('//', 'floordiv'), operator.floordiv),
]

operators = {}
for aliases, func in operator_list:
    for alias in aliases:
        operators[alias] = func


class Op(BaseTag):
    """
    arguments: '`a`, `op`, `b`'
    example: See `tests/test_cond.py`
    description: Performs binary operators. Especially useful with `!If` to implement greater-than etc.
    """
    value_types = (dict, list)
    def enrich(self, context):
        if isinstance(self.data, dict):
            a = context.enrich(self.data['a'])
            op_name = context.enrich(self.data['op'])
            b = context.enrich(self.data['b'])
        elif isinstance(self.data, list):
            assert len(self.data) == 3
            a = context.enrich(self.data[0])
            op_name = context.enrich(self.data[1])
            b = context.enrich(self.data[2])

        op = operators[op_name]

        return op(a, b)
