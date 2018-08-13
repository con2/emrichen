from .base import BaseTag


class With(BaseTag):
    value_types = (dict,)

    def enrich(self, context):
        from ..context import Context

        vars_ = self.data['vars']
        template = self.data['template']

        subcontext = Context(context, vars_)

        return subcontext.enrich(template)
