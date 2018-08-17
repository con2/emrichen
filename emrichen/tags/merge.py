from collections import OrderedDict

from .base import BaseTag


class Merge(BaseTag):
    value_types = (list,)

    def enrich(self, context):
        result = OrderedDict()
        for iterable in self.data:
            result.update(context.enrich(iterable))
        return result
