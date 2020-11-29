from functools import lru_cache
from typing import Any, List

import jsonpath_rw

from ..context import Context
from .base import BaseTag


class EnrichingProxy:
    """
    Eager JSONPath lookups and Emrichen's lazy evaluation don't always mix well.
    Deep nesting with !Var etc. may cause a situation where we try to !Lookup or
    !Format on a structure that is not yet enriched.

    This tries to fix that by enriching property access.

    https://github.com/con2/emrichen/issues/15
    """
    def __init__(self, obj, context):
        self.obj = obj
        self.context = context

    def __getitem__(self, index):
        return self.context.enrich(self.obj[index])


@lru_cache()
def parse_jsonpath(expr: str):
    return jsonpath_rw.parse(expr)


def find_jsonpath_in_context(jsonpath_str: str, context: Context) -> List[jsonpath_rw.DatumInContext]:
    return parse_jsonpath(jsonpath_str).find(EnrichingProxy(context, context))


class Lookup(BaseTag):
    """
    arguments: JSONPath expression
    example: "`!Lookup people[0].first_name`"
    description: Performs a JSONPath lookup returning the first match. If there is no match, an error is raised.
    """
    def enrich(self, context: Context):
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
    def enrich(self, context: Context) -> List[Any]:
        return [context.enrich(m.value) for m in find_jsonpath_in_context(self.data, context)]
