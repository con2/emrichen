import yaml


class BaseMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        yaml.SafeLoader.add_constructor(f'!{name}', cls.load)
        return cls


class BaseTag(metaclass=BaseMeta):
    __slots__ = ['data']

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return f'{self.__class__.__name__}({repr(self.data)})'

    @classmethod
    def load(cls, loader, node):
        data = loader.construct_scalar(node)
        assert isinstance(data, str)
        return cls(data)
