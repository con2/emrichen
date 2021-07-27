from ..context import Context
from .base import BaseTag


class Not(BaseTag):
    """
    arguments: a value
    example: "`!Not !Var foo`"
    description: Logically negates the given value (in Python semantics).
    """

    value_types = (object,)

    def enrich(self, context: Context) -> bool:
        return not context.enrich(self.data)
