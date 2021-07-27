import json
from pprint import pformat
from typing import Any, Callable, Dict

import pyaml
import yaml

from .documents_list import flatten_documents_lists


def render_json(data) -> str:
    if not isinstance(data, list) or len(data) != 1:
        raise TypeError(
            "JSON output can only handle a single document. "
            "A common cause for this error is trying to render a multi-document "
            "YAML template into JSON. If you use a YAML template with JSON output, "
            "it may only contain a single document. !Defaults documents do not count "
            "as they are stripped from the output."
        )

    return json.dumps(data[0], ensure_ascii=False, indent=2)


def render_yaml(data) -> str:
    if isinstance(data, list):
        data = flatten_documents_lists(data)
    return yaml.dump_all(
        data,
        Dumper=pyaml.PrettyYAMLDumper,
        allow_unicode=True,
        default_flow_style=False,
    )


Renderer = Callable[[Any], str]
RENDERERS: Dict[str, Renderer] = {
    'yaml': render_yaml,
    'json': render_json,
    'pprint': pformat,
}


def render(data, format: str) -> str:
    if format in RENDERERS:
        return RENDERERS[format](data)
    else:
        raise ValueError(f'No renderer for format {format}')
