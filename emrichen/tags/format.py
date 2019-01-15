import string

from .base import BaseTag
from .lookup import find_jsonpath_in_context


class JSONPathFormatter(string.Formatter):
    def __init__(self, tag, context):
        super().__init__()
        self.tag = tag
        self.context = context

    def get_field(self, field_name, args, kwargs):
        return (self.context.enrich(self._get_in_context(field_name)), 0)

    def _get_in_context(self, selector):
        matches = find_jsonpath_in_context(selector, self.context)
        if matches:
            return matches[0].value
        else:
            if selector in self.context:  # direct dotted key in context
                return self.context[selector]
        raise KeyError('{self.tag}: {selector} not found in context'.format(
            self=self,
            selector=selector,
        ))


class Format(BaseTag):
    """
    arguments: Format string
    example: '`!Format "{foo} {bar!d}"`'
    description: |
        Interpolate strings using [Python format strings](https://docs.python.org/3/library/string.html#formatstrings).
        JSONPath supported in variable lookup (eg. `{people[0].first_name}` will do the right thing).
        **NOTE:** When the format string starts with `{`, you need to quote it in order to avoid being interpreted as a YAML object.
    """
    def enrich(self, context):
        return JSONPathFormatter(tag=self, context=context).format(self.data)
