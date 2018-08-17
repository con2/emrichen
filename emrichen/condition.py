import operator


operator_list = [
    (('=', '==', '===', 'eq'), operator.eq),
    (('≠', '!=', '!==', 'ne'), operator.ne),
    (('>=', 'ge', 'gte'), operator.ge),
    (('>', 'gt'), operator.gt),
    (('<', 'lt'), operator.lt),
    (('>', 'gt'), operator.gt),
    (('in', '∈'), operator.contains),
    (('not in', '∉'), lambda a, b: not operator.contains(a, b)),
    (('truth', None), lambda a, b: operator.truth(a)),
]

operators = {}
for aliases, func in operator_list:
    for alias in aliases:
        operators[alias] = func


def evaluate_condition(context, cond):
    if 'allOf' in cond:
        return all(evaluate_condition(context, subcond) for subcond in cond['allOf'])
    elif 'anyOf' in cond:
        return any(evaluate_condition(context, subcond) for subcond in cond['anyOf'])

    a = context.enrich(cond['a'])
    b = context.enrich(cond.get('b'))
    op = operators[context.enrich(cond.get('op', 'truth'))]
    negate = context.enrich(cond.get('not'))

    result = op(a, b)
    return (not result if negate else result)
