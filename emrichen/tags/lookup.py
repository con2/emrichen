from .base import BaseTag
from functools import lru_cache
import jsonpath_rw


@lru_cache()
def parse_jsonpath(expr):
    return jsonpath_rw.parse(expr)


def find_jsonpath_in_context(jsonpath_str, context):
    return parse_jsonpath(jsonpath_str).find(context)


class Lookup(BaseTag):
    """
    arguments: JSONPath expression
    example: "`!Lookup people[0].first_name`"
    description: Performs a JSONPath lookup returning the first match. If there is no match, an error is raised.
    """
    def enrich(self, context):
        matches = find_jsonpath_in_context(self.data, context)
        if not matches:
            raise KeyError('{self}: no matches for {self.data}'.format(self=self))
        return context.enrich(matches[0].value)


class LookupAll(BaseTag):
    """
    arguments: JSONPath expression
    example: "`!LookupAll people[*].first_name`"
    description: Performs a JSONPath lookup returning all matches as a list. If no matches are found, the empty list `[]` is returned.
    """
    def enrich(self, context):
        return [context.enrich(m.value) for m in find_jsonpath_in_context(self.data, context)]
