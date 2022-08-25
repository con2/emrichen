from typing import TextIO, Union

from .context import Context
from .tags import Var
from .template import Template

__version__ = '0.3.0'


__all__ = ['Context', 'Template', 'Var', 'emrichen']


def emrichen(template: Union[str, TextIO], *variable_sources, **override_variables) -> str:
    """
    Renders the template using the given variable sources and variable overrides.

    The template can be a string or a readable file-like containing YAML.

    Variable sources can be dict-likes, or strings or readable file-likes containing a
    single YAML document with a single object whose top-level keys will be exported as
    variables.
    """
    c = Context(*variable_sources, **override_variables)
    t = Template.parse(template, 'yaml')

    return t.render(c)
