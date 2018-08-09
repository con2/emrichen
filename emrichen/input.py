import json
from collections import OrderedDict

import yaml

from .tags.base import tag_registry


class RichLoader(yaml.SafeLoader):
    def __init__(self, stream):
        super(RichLoader, self).__init__(stream)
        self.add_tag_constructors()

    def add_tag_constructors(self):
        self.yaml_constructors = self.yaml_constructors.copy()  # Grab an instance copy from the class
        for name, tag in tag_registry.items():
            self.yaml_constructors[f'!{name}'] = tag.load


def _hydrate_json_object(pairs):
    if len(pairs) == 1:
        key, value = pairs[0]
        if key.startswith('!') and key[1:] in tag_registry:
            return tag_registry[key[1:]](value)
    return OrderedDict(pairs)


def json_load_or_loads(str_or_stream, **kwargs):
    if hasattr(str_or_stream, 'read'):
        str_or_stream = str_or_stream.read()
    return json.loads(str_or_stream, **kwargs)


PARSERS = {
    'yaml': lambda data: list(yaml.load_all(data, Loader=RichLoader)),
    'json': lambda data: [json_load_or_loads(data, object_pairs_hook=_hydrate_json_object)],
}


def parse(data, format):
    if format in PARSERS:
        return PARSERS[format](data)
    else:
        raise ValueError(f'No parser for format {format}')
