from ..condition import evaluate_condition
from ..void import Void
from ..utils import maybe_template, maybe_enrich, get_first_key
from .base import BaseTag


class If(BaseTag):
    value_types = (dict,)

    def enrich(self, context):
        true_template = maybe_template(get_first_key(self.data, ('true', True), default=Void))
        false_template = maybe_template(get_first_key(self.data, ('false', False), default=Void))

        if evaluate_condition(context, self.data):
            return maybe_enrich(context, true_template, first=True)
        else:
            return maybe_enrich(context, false_template, first=True)


