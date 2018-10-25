from .base import BaseTag
from .lookup import find_jsonpath_in_context


class Exists(BaseTag):
    """
    arguments: JSONPath expression
    example: "`!Exists foo`"
    description: Returns `true` if the JSONPath expression returns one or more matches, `false` otherwise.
    """
    def enrich(self, context):
        matches = find_jsonpath_in_context(self.data, context)
        return bool(matches)
