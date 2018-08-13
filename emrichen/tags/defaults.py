from .base import BaseTag


class Defaults(BaseTag):
    """
    Defines default values for variables. These will be overridden by any other variable source.

    This is just a holder for the defaults. The actual implementation is in `emrichen.template:enrich`.
    """
    value_types = (dict,)

    def enrich(self, context):
        raise ValueError('Defaults tag is unsupported anywhere else than document root.')
