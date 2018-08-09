from .base import BaseTag
from functools import lru_cache
import jsonpath_rw


@lru_cache()
def parse_jsonpath(expr):
    return jsonpath_rw.parse(expr)


def find_jsonpath_in_context(jsonpath_str, context):
    return parse_jsonpath(jsonpath_str).find(context)


class Lookup(BaseTag):
    def enrich(self, context):
        matches = find_jsonpath_in_context(self.data, context)
        if not matches:
            raise KeyError(f'{self}: no matches for {self.data}')
        return matches[0].value


class LookupAll(BaseTag):
    def enrich(self, context):
        return [m.value for m in find_jsonpath_in_context(self.data, context)]
