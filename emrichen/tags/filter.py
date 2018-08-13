from ..condition import evaluate_condition
from .base import BaseTag
from .loop import get_iterable
from ..void import Void


class Filter(BaseTag):
    value_types = (dict,)

    def enrich(self, context):
        from ..context import Context
        from .lookup import Lookup
        output = []
        as_ = str(self.data.get('as', 'item'))
        index_as = str(self.data.get('index_as') or '')
        test = self.data.get('test', {})
        if 'a' not in test:
            test['a'] = Lookup(as_)
        for index, value in get_iterable(self, self.data.get('over'), context):
            subcontext = {as_: value}
            if index_as:
                subcontext[index_as] = index
            if evaluate_condition(Context(context, subcontext), test):
                if value is not Void:
                    output.append(value)
        return output
