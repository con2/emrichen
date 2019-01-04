from .base import BaseTag


class Var(BaseTag):
    """
    arguments: Variable name
    example: "`!Var image_name`"
    description: Replaced with the value of the variable.
    """
    def enrich(self, context):
        return context.enrich(context[self.data])
