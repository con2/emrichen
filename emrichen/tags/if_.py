from ..condition import evaluate_condition
from ..void import Void
from ..utils import maybe_template, maybe_enrich
from .base import BaseTag


class If(BaseTag):
    value_types = (dict,)

    def enrich(self, context):
        if not ('then' in self.data or 'else' in self.data):
            raise ValueError(f'{self}: missing both then and else')

        true_template = maybe_template(self.data.get('then'), Void)
        false_template = maybe_template(self.data.get('else'), Void)

        if evaluate_condition(context, self.data):
            return maybe_enrich(context, true_template, first=True)
        else:
            return maybe_enrich(context, false_template, first=True)


