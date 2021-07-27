from collections import OrderedDict
from typing import TextIO, Union

import yaml
from yaml.constructor import ConstructorError

from ..exceptions import NoSuchTag
from ..tags.base import BaseTag, tag_registry
from .utils import make_compose


def construct_tagless_yaml(loader: yaml.Loader, node: yaml.Node):
    # From yaml.constructor.BaseConstructor#construct_object
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    elif isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    elif isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)
    raise NotImplementedError('invalid node')


def construct_tagged_object(loader: yaml.Loader, node: yaml.Node) -> BaseTag:
    name = node.tag.lstrip('!')
    if name in tag_registry:
        tag = tag_registry[name]
        data = construct_tagless_yaml(loader, node)
        return tag(data)
    if ',' in name:  # Compose
        try:
            return make_compose(names=name, value=construct_tagless_yaml(loader, node))
        except NoSuchTag as nst:
            name = nst.args[0]
            raise ConstructorError(
                None,
                None,
                f"in compose tag {node.tag}: can't find tag {name}",
                node.start_mark,
            ) from nst
    raise ConstructorError(
        None,
        None,
        f"can't find tag {node.tag}",
        node.start_mark,
    )


class RichLoader(yaml.SafeLoader):
    def __init__(self, stream) -> None:
        super().__init__(stream)
        self.add_tag_constructors()

    def add_tag_constructors(self) -> None:
        self.yaml_constructors = self.yaml_constructors.copy()  # Grab an instance copy from the class
        self.yaml_constructors[self.DEFAULT_MAPPING_TAG] = self._make_ordered_dict
        self.yaml_constructors[None] = construct_tagged_object

    @staticmethod
    def _make_ordered_dict(loader: yaml.Loader, node: yaml.Node) -> OrderedDict:
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))


def load_yaml(data: Union[TextIO, str]):
    return list(yaml.load_all(data, Loader=RichLoader))
