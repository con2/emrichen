from .base import BaseTag


class Defaults(BaseTag):
    """
    arguments: A dict of variable definitions
    example: See `examples/defaults/`
    description: |
        Defines default values for variables. These will be overridden by any other variable source.
        **NOTE:** `!Defaults` must appear in a document of its own in the template file (ie. separated by `---`). \\
        The document containing `!Defaults` will be erased from the output.
    ---
    Defines default values for variables. These will be overridden by any other variable source.

    This is just a holder for the defaults. The actual implementation is in `emrichen.template:enrich`.
    """
    value_types = (dict,)

    def enrich(self, context):
        raise ValueError('Defaults tag is unsupported anywhere else than document root.')
