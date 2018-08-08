import yaml
import pyaml

from .loader import RichLoader
from .context import Context


class Template(object):
    def __init__(self, template):
        self.template = list(yaml.load_all(template, Loader=RichLoader))

    def enrich(self, context):
        if not isinstance(context, Context):
            context = Context(context)

        return context.enrich(self.template)

    def render(self, context):
        enriched = self.enrich(context)
        return yaml.dump_all(enriched, Dumper=pyaml.PrettyYAMLDumper, default_flow_style=False)
