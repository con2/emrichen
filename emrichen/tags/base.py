from typing import Any, Dict, Tuple, Type

tag_registry = {}


class BaseMeta(type):
    def __new__(meta: Type['BaseMeta'], name: str, bases, class_dict: Dict[str, Any]):
        cls = type.__new__(meta, name, bases, class_dict)
        if name[0] != '_' and name != 'BaseTag':
            tag_registry[name] = cls
        return cls


class BaseTag(metaclass=BaseMeta):
    __slots__ = ['data']
    value_types: Tuple[Type, ...] = (str,)

    def __init__(self, data) -> None:
        self.data = data
        if not isinstance(data, self.value_types):
            raise TypeError(f'{self}: data not of valid type (valid types are {self.value_types}')

    def __str__(self) -> str:
        return f'{self.__class__.__name__}.{self.data!r}'
