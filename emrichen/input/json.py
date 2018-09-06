import json
from collections import OrderedDict

from emrichen.tags.base import tag_registry


def _hydrate_json_object(pairs):
    if len(pairs) == 1:
        key, data = pairs[0]
        if key.startswith('!') and key[1:] in tag_registry:
            tag = tag_registry[key[1:]]
            return tag(data)
    return OrderedDict(pairs)


def json_load_or_loads(str_or_stream, **kwargs):
    if hasattr(str_or_stream, 'read'):
        str_or_stream = str_or_stream.read()
    return json.loads(str_or_stream, **kwargs)


def load_json(data):
    return [json_load_or_loads(data, object_pairs_hook=_hydrate_json_object)]
