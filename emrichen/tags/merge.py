from collections import OrderedDict

from .base import BaseTag


class Merge(BaseTag):
    """
    arguments: A list of dicts
    example: '`!Merge [{a: 5}, {b: 6}]`'
    description: Merges objects. For overlapping keys the last one takes precedence.
    """
    value_types = (list, BaseTag)

    def enrich(self, context):
        result = OrderedDict()
        for iterable in context.enrich(self.data):
            result.update(iterable)
        return result
