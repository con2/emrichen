import yaml


class BaseTag:
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

    @classmethod
    def register_tag(cls):
        yaml.SafeLoader.add_constructor(f'!{cls.__name__}', cls.load)
