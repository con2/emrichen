import string

from .base import BaseTag
from .lookup import find_jsonpath_in_context


class JSONPathFormatter(string.Formatter):
    def __init__(self, tag, context):
        super().__init__()
        self.tag = tag
        self.context = context

    def get_field(self, field_name, args, kwargs):
        return (self._get_in_context(field_name), 0)

    def _get_in_context(self, selector):
        matches = find_jsonpath_in_context(selector, self.context)
        if matches:
            return matches[0].value
        else:
            if selector in self.context:  # direct dotted key in context
                return self.context[selector]
        raise KeyError(f'{self.tag}: {selector} not found in context')


class Format(BaseTag):
    def enrich(self, context):
        return JSONPathFormatter(tag=self, context=context).format(self.data)
