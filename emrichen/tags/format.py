from .base import BaseTag


class Format(BaseTag):
    def enrich(self, context):
        return self.data.format_map(context)
