from collections import Mapping, Sequence

from .base import BaseTag


class Loop(BaseTag):
    value_types = (dict,)

    def enrich(self, context):
        from ..context import Context
        from ..template import Template

        as_ = str(self.data.get('as', 'item'))
        index_as = str(self.data.get('index_as') or '')
        compact = bool(self.data.get('compact'))

        template = self.data.get('template')
        if template is None:
            raise ValueError(f'{self}: missing template')
        template = Template([template])

        output = []
        for index, value in self.get_iterable(context):
            subcontext = {as_: value}
            if index_as:
                subcontext[index_as] = index
            value = template.enrich(Context(context, subcontext))[0]
            if compact and not value:
                continue
            output.append(value)
        return output

    def get_iterable(self, context):
        over = self.data.get('over')

        if isinstance(over, str) and over in context:
            # This does mean you can't explicitly iterate over strings that are keys
            # in the context, but if you really do need to do that, you may need to
            # rethink your approach anyway.
            raise ValueError(
                f'{self}: `over` value exists within the context; did you mean `!Var {over}`?'
            )

        if hasattr(over, 'enrich'):
            over = over.enrich(context)
        if isinstance(over, Mapping):
            return over.items()
        elif isinstance(over, Sequence):
            return enumerate(over)

        raise ValueError(f'{self}: over value {over} is not iterable')
