from .base import BaseTag


class Defaults(BaseTag):
    value_types = (dict,)

    def enrich(self, context):
        raise ValueError('Defaults tag is unsupported anywhere else than document root.')
