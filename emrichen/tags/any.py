from .base import BaseTag


class Any(BaseTag):
    value_types = (list,)

    def enrich(self, context):
        return any(context.enrich(item) for item in self.data)
