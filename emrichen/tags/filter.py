from collections import OrderedDict

from ..condition import evaluate_condition
from .base import BaseTag
from .loop import get_iterable
from ..void import Void


class Filter(BaseTag):
    value_types = (dict,)

    def enrich(self, context):
        from ..context import Context
        from .lookup import Lookup
        as_ = str(self.data.get('as', 'item'))
        index_as = str(self.data.get('index_as') or '')
        test = self.data.get('test', {})
        if 'a' not in test:
            test['a'] = Lookup(as_)
        iterable, is_mapping = get_iterable(self, self.data.get('over'), context)
        output = (OrderedDict() if is_mapping else [])
        for index, value in iterable:
            subcontext = {as_: value}
            if index_as:
                subcontext[index_as] = index
            if evaluate_condition(Context(context, subcontext), test):
                if value is Void:
                    continue
                if is_mapping:
                    output[index] = value
                else:
                    output.append(value)
        return output
