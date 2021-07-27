from functools import lru_cache
from typing import Any, List

import jsonpath_rw

from ..context import Context
from .base import BaseTag


@lru_cache()
def parse_jsonpath(expr: str):
    return jsonpath_rw.parse(expr)


def find_jsonpath_in_context(jsonpath_str: str, context: Context) -> List[jsonpath_rw.DatumInContext]:
    return parse_jsonpath(jsonpath_str).find(context)


class Lookup(BaseTag):
    """
    arguments: JSONPath expression
    example: "`!Lookup people[0].first_name`"
    description: Performs a JSONPath lookup returning the first match. If there is no match, an error is raised.
    """

    def enrich(self, context: Context):
        matches = find_jsonpath_in_context(self.data, context)
        if not matches:
            raise KeyError(f'{self}: no matches for {self.data}')
        return context.enrich(matches[0].value)


class LookupAll(BaseTag):
    """
    arguments: JSONPath expression
    example: "`!LookupAll people[*].first_name`"
    description: Performs a JSONPath lookup returning all matches as a list. If no matches are found, the empty list `[]` is returned.
    """

    def enrich(self, context: Context) -> List[Any]:
        return [context.enrich(m.value) for m in find_jsonpath_in_context(self.data, context)]
