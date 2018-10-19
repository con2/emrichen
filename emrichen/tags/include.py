import os

from .base import BaseTag
from ..void import Void


class Include(BaseTag):
    def enrich(self, context):
        from ..template import Template

        include_path = os.path.join(os.path.dirname(context['__file__']), self.data)
        with open(include_path) as include_file:
            # TODO: determine format (now YAML only)
            include_template = Template.parse(include_file)

        enriched = include_template.enrich(context)

        if len(enriched) == 0:
            return Void
        if len(enriched) > 1:
            raise ValueError('!Include can only include single-document templates')

        return enriched[0]
