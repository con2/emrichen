from typing import TextIO, Union

from .json import load_json
from .yaml import load_yaml

PARSERS = {
    'yaml': load_yaml,
    'json': load_json,
}


def parse(data: Union[TextIO, str], format: str):
    if format in PARSERS:
        return PARSERS[format](data)
    else:
        raise ValueError(f'No parser for format {format}')
