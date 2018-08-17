from ..condition import evaluate_condition
from ..void import Void
from .base import BaseTag


class If(BaseTag):
    value_types = (dict,)

    def enrich(self, context):
        if not ('then' in self.data or 'else' in self.data):
            raise ValueError(f'{self}: missing both then and else')

        true_template = self.data.get('then', Void)
        false_template = self.data.get('else', Void)

        if evaluate_condition(context, self.data):
            return context.enrich(true_template)
        else:
            return context.enrich(false_template)


