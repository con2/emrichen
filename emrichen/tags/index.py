from collections import OrderedDict
from sys import stderr

from .loop import Loop
from .var import Var


class _BaseIndex(Loop):
    value_types = (dict,)
    output_factory = OrderedDict

    def __init__(self, data):
        if 'template' not in data:
            as_ = data.get('as', 'item')
            data = dict(data, template=Var(as_))

        super(_BaseIndex, self).__init__(data)


class Index(_BaseIndex):
    """
    arguments: |
        Accepts the same arguments as `!Loop`, except `template` is optional (default identity), plus the following:
        `by`: (required) An expression used to determine the key for the current value
        `result_as`: (optional, string) When evaluating `by`, the enriched `template` is available under this name.
        `duplicates`: (optional, default `error`) `error`, `warn(ing)` or `ignore` duplicate values.

    example: TBD
    description: Makes a dict out of a list. Keys are determined by `by`.
    """
    def __init__(self, data):
        if 'template' not in data:
            as_ = data.get('as', 'item')
            data = dict(data, template=Var(as_))

        super(Index, self).__init__(data)

    def process_item(self, context, output, value, result):
        from ..context import Context

        by = self.data['by']
        result_as = self.data.get('result_as')

        if result_as:
            context = Context(context, {result_as: result})

        key = context.enrich(by)

        if key in output:
            # Duplicate key
            action = self.data.get('duplicates', 'error')
            message = '{self}: Duplicate key {key!r}'.format(self=self, key=key)
            if action == 'warn':
                # TODO logger
                stderr.write(message + '\n')
            elif action == 'error':
                raise ValueError(message)

        output[key] = result


class Group(_BaseIndex):
    """
    arguments: |
        Accepts the same arguments as `!Loop`, except `template` is optional (default identity), plus the following:
        `by`: (required) An expression used to determine the key for the current value
        `result_as`: (optional, string) When evaluating `by`, the enriched `template` is available under this name.

    example: TBD
    description: Makes a dict out of a list. Keys are determined by `by`. Items with the same key are grouped in a list.
    """
    def process_item(self, context, output, value, result):
        from ..context import Context

        by = self.data['by']
        result_as = self.data.get('result_as')

        if result_as:
            context = Context(context, {result_as: result})

        key = context.enrich(by)
        group = output.setdefault(key, [])
        group.append(result)
