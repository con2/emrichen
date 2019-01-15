from .base import BaseTag


class Any(BaseTag):
    """
    arguments: An iterable
    example: "`!Any [true, false]`"
    description: Returns true iff at least one of the items of the iterable argument is truthy.
    """
    value_types = (list, BaseTag)

    def enrich(self, context):
        return any(context.enrich(item) for item in self.data)
