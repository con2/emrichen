from .context import Context, VariableExtractorContext
from .input import parse
from .output import render
from .tags import Defaults


class Template(object):
    def __init__(self, template):
        if not isinstance(template, list):
            raise TypeError(
                f'`template` must be a list of objects; {template!r} is not. '
                f'Are you maybe looking for Template.parse()?'
            )

        self.template, self.defaults = extract_defaults(template)

    def enrich(self, context):
        context = Context(self.defaults, context)
        return context.enrich(self.template)

    def render(self, context, format='yaml'):
        enriched = self.enrich(context)
        return render(enriched, format)

    def get_vars(self, context=Context()):
        context = VariableExtractorContext(context)
        self.enrich(context)
        return context

    def print_vars(self, context=Context(), format='yaml'):
        context = self.get_vars(context)
        return render(context, format)

    @classmethod
    def parse(cls, data, format):
        return cls(template=parse(data, format=format))


def extract_defaults(template):
    defaults = {}
    for doc in template:
        if isinstance(doc, Defaults):
            defaults.update(doc.data)

    template = [doc for doc in template if not isinstance(doc, Defaults)]

    return template, defaults
