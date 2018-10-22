from .base import BaseTag


class Not(BaseTag):
    value_types = (object,)

    def enrich(self, context):
        return not context.enrich(self.data)
