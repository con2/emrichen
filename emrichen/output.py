import json

import pyaml
import yaml

RENDERERS = {
    'yaml': lambda data: yaml.dump_all(data, Dumper=pyaml.PrettyYAMLDumper, default_flow_style=False),
    'json': lambda data: json.dumps(data, ensure_ascii=False, indent=2),
}


def render(data, format):
    if format in RENDERERS:
        return RENDERERS[format](data)
    else:
        raise ValueError(f'No renderer for format {format}')
