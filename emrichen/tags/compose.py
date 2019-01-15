from .base import BaseTag, tag_registry


class Compose(BaseTag):
    '''
    arguments: |
        `value`: The value to apply tags on
        `tags`: A list of tag names to apply, latest first
    example: |
        `!Base64,Var foo`
    description: |
        Used internally to implement tag composition.
        Usually not used in the spelt-out form.
        See _Tag composition_ below.
    '''
    value_types = (dict,)

    def enrich(self, context):
        value = self.data.get('value')
        for tag_name in reversed(self.data['tags']):
            tag_class = tag_registry[tag_name]
            value = tag_class(value)
        return context.enrich(value)
