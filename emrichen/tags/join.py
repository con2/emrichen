from collections.abc import Mapping

from .base import BaseTag


class Join(BaseTag):
    """
    arguments: |
        `items`: (required) A list of items to be joined together.
        `separator`: (optional, default space) The separator to place between the items.
        **OR**
        a list of items to be joined together with a space as the separator.
    example: |
        `!Join [foo, bar]`
        `!Join { items: [foo, bar], separator: ', ' }`
    description: Joins a list of items together with a separator. The result is always a string.
    """

    value_types = (dict, list, BaseTag)

    def enrich(self, context):
        if isinstance(self.data, Mapping):
            separator = context.enrich(self.data.get('separator', ' '))
            items = context.enrich(self.data['items'])
        else:
            separator = ' '
            items = context.enrich(self.data)
            if not isinstance(items, list):
                raise TypeError('{self}: must resolve to a list'.format(self=self))

        return separator.join(str(i) for i in items)
