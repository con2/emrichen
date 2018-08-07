import yaml


class Var:
    __slots__ = ['name']

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'Var({repr(self.name)})'

    def enrich(self, context):
        return context[self.name]

    @classmethod
    def load(cls, loader, node):
        name = loader.construct_scalar(node)
        assert isinstance(name, str)
        return cls(name)


yaml.SafeLoader.add_constructor('!Var', Var.load)
