import os

from .base import BaseTag
from ..void import Void


class Include(BaseTag):
    def get_template(self, context):
        from ..template import Template

        include_path = os.path.join(
            os.path.dirname(context['__file__']), self.data)

        with open(include_path) as include_file:
            return Template.parse(include_file)

    def enrich(self, context):
        template = self.get_template(context)
        enriched = template.enrich(context)

        if len(enriched) == 0:
            return Void
        if len(enriched) > 1:
            raise ValueError('!Include can only include single-document templates')

        return enriched[0]
