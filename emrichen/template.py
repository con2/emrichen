import os
from typing import Mapping, Optional, TextIO, Tuple, Union

from .context import Context
from .output import Renderer, render


def determine_format(filename: Optional[str], choices: Mapping[str, Renderer], default: str) -> str:
    if filename:
        ext = os.path.splitext(filename)[1].lstrip('.').lower()
        if ext in choices:
            return ext
    return default


class Template:
    def __init__(self, template, filename: Optional[str] = None) -> None:
        if not isinstance(template, list):
            raise TypeError(
                f'`template` must be a list of objects; {template!r} is not. Are you maybe looking for Template.parse()?'
            )

        self.template, self.defaults = extract_defaults(template, filename)
        self.filename = filename

    def enrich(self, context: Union[dict, Context]):
        context = Context(self.defaults, context, __file__=self.filename)
        return context.enrich(self.template)

    def render(self, context: Union[dict, Context], format: str = 'yaml') -> str:
        enriched = self.enrich(context)
        return render(enriched, format)

    @classmethod
    def parse(
        cls,
        data: Union[TextIO, str],
        format: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> 'Template':
        from .input import PARSERS, parse

        if filename is None and hasattr(data, 'name') and data.name:  # type: ignore
            filename = data.name  # type: ignore

        if format is None:
            format = determine_format(filename, PARSERS, 'yaml')

        return cls(template=parse(data, format=format), filename=filename)


def extract_defaults(template, filename: Optional[str]) -> Tuple[list, dict]:
    from .tags import Defaults, Include

    defaults = {}

    for doc in template:
        if isinstance(doc, Defaults):
            defaults.update(doc.data)
        elif isinstance(doc, Include):
            temp_context = Context()
            temp_context.update(defaults, __file__=filename)
            defaults.update(doc.get_template(temp_context).defaults)

    template = [doc for doc in template if not isinstance(doc, Defaults)]

    return template, defaults
