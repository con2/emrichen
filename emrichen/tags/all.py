from .base import BaseTag


class All(BaseTag):
    value_types = (list,)

    def enrich(self, context):
        return all(context.enrich(item) for item in self.data)
