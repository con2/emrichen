from collections import OrderedDict

from .base import BaseTag


class Merge(BaseTag):
    """
    arguments: A list of dicts
    example: '`!Merge [{a: 5}, {b: 6}]`'
    description: Merges objects. For overlapping keys the last one takes precedence.
    """
    value_types = (list,)

    def enrich(self, context):
        result = OrderedDict()
        for iterable in self.data:
            result.update(context.enrich(iterable))
        return result
