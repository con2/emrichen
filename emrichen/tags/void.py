from ..void import Void as VoidObj
from .base import BaseTag


class Void(BaseTag):
    """
    arguments: Anything or nothing
    example: "`foo: !Void`"
    description: The dict key, list item or YAML document that resolves to `!Void` is removed from the output.
    """
    value_types = (object,)
    def enrich(self, context):
        return VoidObj
