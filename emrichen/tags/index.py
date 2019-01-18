from collections import OrderedDict
from sys import stderr

from .loop import Loop
from .var import Var


class Index(Loop):
    """
    arguments: |
        Accepts the same arguments as `!Loop`, except `template` is optional (default identity), plus the following:
        `by`: (required) An expression used to determine the key for the current value
        `result_as`: (optional, string) When evaluating `by`, the enriched `template` is available under this name.
        `duplicates`: (optional, default `error`) `error`, `warn(ing)` or `ignore` duplicate values.

    example: TBD
    description: Makes a dict out of a list. Keys are determined by `by`.
    """
    value_types = (dict,)

    def enrich(self, context):
        as_ = self.data.get('as', 'item')

        if 'template' not in self.data:
            self.data = dict(self.data, template=Var(as_))

        self._index = OrderedDict()
        super(Index, self).enrich(context)
        return self._index

    def process_item(self, context, value, result):
        from ..context import Context

        by = self.data['by']
        result_as = self.data.get('result_as')

        if result_as:
            context = Context(context, {result_as: result})

        key = context.enrich(by)

        if key in self._index:
            # Duplicate key
            action = self.data.get('duplicates', 'error')
            message = '{self}: Duplicate key {key!r}'.format(self=self, key=key)
            if action == 'warn':
                # TODO logger
                stderr.write(message + '\n')
            elif action == 'error':
                raise ValueError(message)

        self._index[key] = result
