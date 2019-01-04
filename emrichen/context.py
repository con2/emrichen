from collections import OrderedDict
from collections.abc import Mapping, Sequence

from .input import parse
from .void import Void


class Context(dict):
    """
    The Context loads variables from various variable sources and enriches
    YAML values using them.
    """

    def __init__(self, *variable_sources, **override_variables):
        self.add_variables(*variable_sources, **override_variables)

    def enrich(self, value):
        """
        Given a YAML value, performs our registered transformations on it.
        """
        if hasattr(value, 'enrich'):
            return value.enrich(self)

        # need to special-case str before Sequence because str \subset Sequence
        elif isinstance(value, str):
            return value

        elif isinstance(value, Mapping):
            out = OrderedDict()
            for key, val in value.items():
                val = self.enrich(val)
                if val is not Void:
                    out[key] = val
            return out
        elif isinstance(value, Sequence):
            out = []
            for item in value:
                item = self.enrich(item)
                if item is not Void:
                    out.append(item)
            return out
        else:
            return value

    def add_variables(self, *variable_sources, **override_variables):
        """
        Adds one or more sources of variables into this Context. If the same variable is defined
        by multiple sources, the last one takes precedence.

        Variable sources can be dict-likes, or strings or readable file-likes containing a
        single YAML document with a single object whose top-level keys will be exported as
        variables.
        """
        for variables in variable_sources:
            if isinstance(variables, Mapping):
                self.update(variables)
            else:
                for yaml_document in parse(variables, 'yaml'):
                    self.update(yaml_document)

        self.update(override_variables)
