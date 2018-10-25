from .base import BaseTag


class Error(BaseTag):
    """
    arguments: Error message
    example: '`!Error "Must define either foo or bar, not both"`'
    description: |
        If the `!Error` tag is present in the template after resolving all conditionals,
        it will cause the template rendering to exit with error emitting the specified error message.
    ---
    This tag, when enriched, emits an user-specified error message and exits.
    """
    def enrich(self, context):
        raise ValueError(self.data)
