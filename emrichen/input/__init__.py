from .json import load_json
from .yaml import load_yaml

PARSERS = {
    'yaml': load_yaml,
    'json': load_json,
}


def parse(data, format):
    if format in PARSERS:
        return PARSERS[format](data)
    else:
        raise ValueError('No parser for format {format}'.format(format=format))
