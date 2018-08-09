tag_registry = {}


class BaseMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        tag_registry[name] = cls
        return cls


class BaseTag(metaclass=BaseMeta):
    __slots__ = ['data']
    value_types = (str,)

    def __init__(self, data):
        self.data = data
        if not isinstance(data, self.value_types):
            raise TypeError(f'{self}: data not of valid type (valid types are {self.value_types}')

    def __str__(self):
        return f'{self.__class__.__name__}({repr(self.data)})'
