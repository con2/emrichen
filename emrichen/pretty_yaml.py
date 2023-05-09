# Based on https://github.com/mk-fg/pretty-yaml/blob/34581d45859ac7e38cdb26f4da5ce1782c3052d7/pyaml/__init__.py
# which is licensed under the WTFPLv2 license.

from __future__ import annotations

import collections
import pathlib

import yaml


def pyaml_transliterate(string: str) -> str:
    string_new = ""
    for ch in string:
        if ch.isalnum() or ch in "-_":
            string_new += ch
        else:
            string_new += "_"
    return string_new.lower()


class PrettyYAMLDumper(yaml.dumper.SafeDumper):
    def __init__(self, *args, **kwargs) -> None:
        self.pyaml_sort_dicts = kwargs.pop("sort_dicts", True)
        super().__init__(*args, **kwargs)

    def represent_odict(self, data):
        value = []
        node = yaml.nodes.MappingNode("tag:yaml.org,2002:map", value, flow_style=None)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        for item_key, item_value in data.items():
            node_key = self.represent_data(item_key)
            node_value = self.represent_data(item_value)
            value.append((node_key, node_value))
        node.flow_style = False
        return node

    def represent_undefined(self, data):
        if isinstance(data, tuple) and hasattr(data, "_make") and hasattr(data, "_asdict"):
            return self.represent_odict(data._asdict())  # assuming namedtuple
        if isinstance(data, collections.OrderedDict):
            return self.represent_odict(data)
        if isinstance(data, dict):
            return self.represent_dict(data)
        if callable(getattr(data, "tolist", None)):
            return self.represent_data(data.tolist())
        return super().represent_undefined(data)

    def represent_dict(self, data):
        if not self.pyaml_sort_dicts:
            return self.represent_odict(data)
        return super().represent_dict(data)

    def anchor_node(self, node, hint: list | None = None):
        if node in self.anchors:
            if self.anchors[node] is None:
                self.anchors[node] = (
                    self.generate_anchor(node)
                    if not hint
                    else pyaml_transliterate("_-_".join(el.value for el in hint))
                )
        else:
            self.anchors[node] = None
            if isinstance(node, yaml.nodes.SequenceNode):
                for item in node.value:
                    self.anchor_node(item)
            elif isinstance(node, yaml.nodes.MappingNode):
                for key, value in node.value:
                    self.anchor_node(key)
                    self.anchor_node(value, hint=(hint or []) + [key])


PrettyYAMLDumper.add_representer(dict, PrettyYAMLDumper.represent_dict)
PrettyYAMLDumper.add_representer(collections.defaultdict, PrettyYAMLDumper.represent_dict)
PrettyYAMLDumper.add_representer(collections.OrderedDict, PrettyYAMLDumper.represent_odict)
PrettyYAMLDumper.add_representer(set, PrettyYAMLDumper.represent_list)
PrettyYAMLDumper.add_representer(None, PrettyYAMLDumper.represent_undefined)  # type: ignore[arg-type]
PrettyYAMLDumper.add_representer(type(pathlib.Path("")), lambda cls, o: cls.represent_data(str(o)))
