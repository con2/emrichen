from base64 import b64encode

from .base import BaseTag


class Base64(BaseTag):
    """
    arguments: The value to encode
    example: "`!Base64 foobar`"
    description: Encodes the value (or a string representation thereof) into base64.
    """
    value_types = (object,)

    def enrich(self, context):
        data = context.enrich(self.data)

        if not isinstance(data, bytes):
            data = str(data).encode('UTF-8')

        return b64encode(data).decode('UTF-8')
