from .context import Context
from .template import Template
from .tags import Var


__all__ = [
    'Context',
    'Template',
    'Var',
    'emrichen',
]


def emrichen(template, *variable_sources, **override_variables):
    """
    Renders the template using the given variable sources and variable overrides.

    The template can be a string or a readable file-like containing YAML.
    """
    c = Context(*variable_sources, **override_variables)
    t = Template(template)

    return t.render(c)

