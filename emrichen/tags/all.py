from .base import BaseTag


class All(BaseTag):
    """
    arguments: An iterable
    example: "`!All [true, false]`"
    description: Returns true iff all the items of the iterable argument are truthy.
    """
    value_types = (list, BaseTag)

    def enrich(self, context):
        return all(context.enrich(item) for item in self.data)
