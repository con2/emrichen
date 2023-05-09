from collections import OrderedDict
from typing import Mapping, Union

from ..context import Context
from ..void import Void
from .base import BaseTag
from .loop import get_iterable
from .var import Var


class Filter(BaseTag):
    """
    arguments: "`test`, `over`"
    example: See `tests/test_cond.py`
    description: Takes in a list and only returns elements that pass a predicate.
    """

    value_types = (dict,)

    def enrich(self, context: Context):
        as_ = str(self.data.get('as', 'item'))
        index_as = str(self.data.get('index_as') or '')
        test = self.data.get('test', Var(as_))
        iterable, is_mapping = get_iterable(self, self.data['over'], context)

        output: Union[OrderedDict, list] = OrderedDict() if is_mapping else []

        for index, value in iterable:
            subcontext = {as_: value}
            if index_as:
                subcontext[index_as] = index

            if Context(context, subcontext).enrich(test):
                if value is Void:
                    continue
                if isinstance(output, Mapping):
                    output[index] = value
                elif isinstance(output, list):
                    output.append(value)
                else:
                    raise NotImplementedError('invalid output type')

        return output
