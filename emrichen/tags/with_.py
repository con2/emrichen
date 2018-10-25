from .base import BaseTag


class With(BaseTag):
    """
    arguments: |
        `vars`: A dict of variable definitions.
        `template`: The template to process with the variables defined.
    example: See `examples/with/`.
    description: Binds local variables that are only visible within `template`. Useful for giving a name for common sub-expressions.
    """
    value_types = (dict,)

    def enrich(self, context):
        from ..context import Context

        vars_ = self.data['vars']
        template = self.data['template']

        subcontext = Context(context, vars_)

        return subcontext.enrich(template)
