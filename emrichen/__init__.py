from collections.abc import Mapping, Sequence
from collections import namedtuple, OrderedDict
import sys

import yaml
import pyaml


class Var(object):
    __slots__ = ['name']

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'Var({repr(self.name)})'

    @classmethod
    def load(cls, loader, node):
        name = loader.construct_scalar(node)
        assert isinstance(name, str)
        return cls(name)


yaml.SafeLoader.add_constructor('!Var', Var.load)


class Template(object):
    def __init__(self, template):
        self.template = list(yaml.safe_load_all(template))

    def enrich(self, context):
        if not isinstance(context, Context):
            context = Context(context)

        return context.enrich(self.template)

    def render(self, context):
        enriched = self.enrich(context)
        return yaml.dump_all(enriched, Dumper=pyaml.PrettyYAMLDumper, default_flow_style=False)


class Context(object):
    def __init__(self, *variable_sources, **override_variables):
        self.variables = dict()
        self.add_variables(*variable_sources, **override_variables)

    def __getitem__(self, key):
        return self.variables[key]

    def enrich(self, value):
        if isinstance(value, Var):
            return self.enrich(self[value.name])

        # need to special-case str before Sequence because str \subset Sequence
        elif isinstance(value, str):
            return value

        elif isinstance(value, Mapping):
            return dict((key, self.enrich(val)) for (key, val) in value.items())
        elif isinstance(value, Sequence):
            return [self.enrich(item) for item in value]
        else:
            return value

    def add_variables(self, *variable_sources, **override_variables):
        """
        Adds one or more sources of variables into this Context.
        If the same variable is defined by multiple sources,
        the last one takes precedence.
        """

        for variables in variable_sources:
            if not isinstance(variables, Mapping):
                variables = yaml.safe_load(variables)

            self.variables.update(variables)

        self.variables.update(override_variables)


def emrichen(template, *variable_sources, **override_variables):
    c = Context(*variable_sources, **override_variables)
    t = Template(template)

    return t.render(c)

