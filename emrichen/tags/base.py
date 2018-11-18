tag_registry = {}


class BaseMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        if name[0] != '_' and name != 'BaseTag':
            tag_registry[name] = cls
        return cls


class BaseTag(metaclass=BaseMeta):
    __slots__ = ['data']
    value_types = (str,)

    def __init__(self, data):
        self.data = data
        if not isinstance(data, self.value_types):
            raise TypeError('{self}: data not of valid type (valid types are {self.value_types}'.format(self=self))

    def __str__(self):
        return '{classname}.{data}'.format(
            classname=self.__class__.__name__,
            data=repr(self.data),
        )
