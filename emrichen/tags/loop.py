from collections.abc import Mapping, Sequence

from ..documents_list import DocumentsList
from .base import BaseTag


def get_iterable(tag, over, context, index_start=None):
    if isinstance(over, str) and over in context:
        # This does mean you can't explicitly iterate over strings that are keys
        # in the context, but if you really do need to do that, you may need to
        # rethink your approach anyway.
        raise ValueError(
            '{tag}: `over` value exists within the context; did you mean `!Var {over}`?'.format(
                tag=tag,
                over=over,
            )
        )

    if hasattr(over, 'enrich'):
        over = over.enrich(context)

    if isinstance(over, Mapping):
        if index_start is not None:
            raise ValueError('cannot use index_start with dict')

        return (over.items(), True)

    if isinstance(over, Sequence):
        if index_start is None:
            index_start = 0

        return (enumerate(over, index_start), False)

    raise ValueError('{tag}: over value {over} is not iterable'.format(tag=tag, over=over))


class Loop(BaseTag):
    """
    arguments: |
        `over`: (required) The data to iterate over (a literal list or dict, or !Var)
        `as`: (optional, default `item`) The variable name given to the current value
        `index_as`: (optional) The variable name given to the loop index. If over is a list, this is a numeric index starting from `0`. If over is a dict, this is the dict key.
        `index_start`: (optional, default `0`) First index, for eg. 1-based indexing.
        `previous_as`: (optional) The variable name given to the previous value. On the first iteration of the loop, the previous value is `null`. _Added in 0.2.0_
        `template`: (required) The template to process for each iteration of the loop.
        `as_documents`: (optional) Whether to "unfold" the output of this loop into separate YAML documents when writing YAML. Only has an effect at the top level of a template.
    example: See `examples/loop/`.
    description: Loops over a list or dict and renders a template for each iteration. The output is always a list.
    """
    value_types = (dict,)
    output_factory = list

    def enrich(self, context):
        from ..context import Context

        as_ = str(self.data.get('as', 'item'))
        index_as = str(self.data.get('index_as') or '')
        compact = bool(self.data.get('compact'))
        index_start = self.data.get('index_start')
        previous_as = str(self.data.get('previous_as') or '')
        as_documents = bool(self.data.get('as_documents'))

        if as_documents:
            self.output_factory = DocumentsList

        template = self.data.get('template')
        if template is None:
            raise ValueError('{self}: missing template'.format(self=self))

        output = self.output_factory()
        iterable, _ = self.get_iterable(context, index_start)
        previous_value = None
        for index, value in iterable:
            subcontext = {as_: value}
            if index_as:
                subcontext[index_as] = index
            if previous_as:
                subcontext[previous_as] = previous_value
            subcontext = Context(context, subcontext)

            result = subcontext.enrich(template)
            previous_value = value

            if compact and not result:
                continue

            self.process_item(subcontext, output, value, result)
        return output

    def get_iterable(self, context, index_start):
        return get_iterable(self, self.data.get('over'), context, index_start)

    def process_item(self, context, output, value, result):
        '''
        Used by Loop subclasses to do things every iteration.
        '''
        output.append(result)
