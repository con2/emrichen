import json
from collections import OrderedDict
from typing import Any, List, TextIO, Union

from ..exceptions import NoSuchTag
from ..tags.base import tag_registry
from .utils import make_compose


def _hydrate_json_object(pairs: Any) -> Any:
    if len(pairs) == 1:
        key, data = pairs[0]
        if key.startswith('!'):
            key = key[1:]
            if ',' in key:
                try:
                    return make_compose(names=key, value=data)
                except NoSuchTag as nst:
                    raise NameError("in compose tag {}: can't find tag {}".format(key, nst.args[0])) from nst
            if key not in tag_registry:
                raise NoSuchTag(key)
            return tag_registry[key](data)
    return OrderedDict(pairs)


def json_load_or_loads(str_or_stream: Union[TextIO, str], **kwargs) -> Any:
    if hasattr(str_or_stream, 'read'):
        str_or_stream = str_or_stream.read()
    return json.loads(str_or_stream, **kwargs)


def load_json(data: Union[TextIO, str]) -> List[Any]:
    return [json_load_or_loads(data, object_pairs_hook=_hydrate_json_object)]
