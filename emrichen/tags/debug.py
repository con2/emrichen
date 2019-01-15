import sys

from .base import BaseTag


class Debug(BaseTag):
    """
    arguments: Anything, really
    example: '`!Debug,Var foo`'
    description: |
        Enriches its argument, outputs it to stderr and returns it. Useful to check the value
        of some expression deep in a big template, perhaps even one that doesn't even fully render.
    """

    value_types = (object,)

    def enrich(self, context):
        value = context.enrich(self.data)
        sys.stderr.write(str(value) + '\n')
        return value
