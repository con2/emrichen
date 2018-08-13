from .base import BaseTag


class Error(BaseTag):
    """
    This tag, when enriched, emits an user-specified error message and exits.
    """
    def enrich(self, context):
        raise ValueError(self.data)
