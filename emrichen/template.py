from .output import render
from .context import Context
from .input import parse


class Template(object):
    def __init__(self, template):
        if not isinstance(template, list):
            raise TypeError(
                f'`template` must be a list of objects; {template!r} is not. '
                f'Are you maybe looking for Template.parse()?'
            )
        self.template = template

    def enrich(self, context):
        if not isinstance(context, Context):
            context = Context(context)

        return context.enrich(self.template)

    def render(self, context, format='yaml'):
        enriched = self.enrich(context)
        return render(enriched, format)

    @classmethod
    def parse(cls, data, format):
        return cls(template=parse(data, format=format))
