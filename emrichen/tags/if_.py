from ..void import Void
from .base import BaseTag


class If(BaseTag):
    """
    arguments: '`test`, `then`, `else`'
    example: "See `tests/test_cond.py`"
    description: Returns one of two values based on a condition.
    """
    value_types = (dict,)

    def enrich(self, context):
        if 'test' not in self.data:
            raise ValueError('{self}: missing test'.format(self=self))

        if not ('then' in self.data or 'else' in self.data):
            raise ValueError('{self}: missing both then and else'.format(self=self))

        true_template = self.data.get('then', Void)
        false_template = self.data.get('else', Void)
        test = self.data['test']

        if context.enrich(test):
            return context.enrich(true_template)
        else:
            return context.enrich(false_template)


