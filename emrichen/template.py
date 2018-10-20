import os

from .context import Context
from .input import parse, PARSERS
from .output import render
from .tags import Defaults


def determine_format(filename, choices, default):
    if filename:
        ext = os.path.splitext(filename)[1].lstrip('.').lower()
        if ext in choices:
            return ext
    return default


class Template(object):
    def __init__(self, template, filename=None):
        if not isinstance(template, list):
            raise TypeError(
                f'`template` must be a list of objects; {template!r} is not. '
                f'Are you maybe looking for Template.parse()?'
            )

        self.template, self.defaults = extract_defaults(template)
        self.filename = filename

    def enrich(self, context):
        context = Context(self.defaults, context, __file__=self.filename)
        return context.enrich(self.template)

    def render(self, context, format='yaml'):
        enriched = self.enrich(context)
        return render(enriched, format)

    @classmethod
    def parse(cls, data, format=None, filename=None):
        if filename is None and hasattr(data, 'name') and data.name:
            filename = data.name

        if format is None:
            format = determine_format(filename, PARSERS, 'yaml')

        return cls(template=parse(data, format=format), filename=filename)


def extract_defaults(template):
    defaults = {}
    for doc in template:
        if isinstance(doc, Defaults):
            defaults.update(doc.data)

    template = [doc for doc in template if not isinstance(doc, Defaults)]

    return template, defaults
