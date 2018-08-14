from .base import BaseTag
from .lookup import find_jsonpath_in_context


class Exists(BaseTag):
    def enrich(self, context):
        matches = find_jsonpath_in_context(self.data, context)
        return bool(matches)
