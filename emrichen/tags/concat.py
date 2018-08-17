from .base import BaseTag


class Concat(BaseTag):
    value_types = (list,)

    def enrich(self, context):
        result = []
        for iterable in self.data:
            result.extend(context.enrich(iterable))
        return result
