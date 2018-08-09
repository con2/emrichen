from collections.abc import Mapping, Sequence

from emrichen.input import parse


class Context(object):
    """
    The Context loads variables from various variable sources and enriches
    YAML values using them.
    """

    def __init__(self, *variable_sources, **override_variables):
        self.variables = dict()
        self.add_variables(*variable_sources, **override_variables)

    def __getitem__(self, key):
        return self.variables[key]

    def enrich(self, value):
        """
        Given a YAML value, performs our registered transformations on it.
        """
        if hasattr(value, 'enrich'):
            return self.enrich(value.enrich(self))

        # need to special-case str before Sequence because str \subset Sequence
        elif isinstance(value, str):
            return value

        elif isinstance(value, Mapping):
            return {key: self.enrich(val) for (key, val) in value.items()}
        elif isinstance(value, Sequence):
            return [self.enrich(item) for item in value]
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
            if not isinstance(variables, Mapping):
                variables = parse(variables, 'yaml')[0]

            self.variables.update(variables)

        self.variables.update(override_variables)
