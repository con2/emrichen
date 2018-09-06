from .base import BaseTag, tag_registry


class Compose(BaseTag):
    value_types = (dict,)

    def enrich(self, context):
        value = context.enrich(self.data.get('value'))
        for tag_name in self.data['tags'][::-1]:
            tag_class = tag_registry[tag_name]
            value = context.enrich(tag_class(value))
        return value
