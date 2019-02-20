from numbers import Number

from emrichen.void import Void
from .base import BaseTag


class _BaseIsType(BaseTag):
    """
    arguments: Data to typecheck.
    example: "`!{name} ...`"
    description: Returns True if the value enriched is of the given type, False otherwise.
    """
    requisite_type = None
    value_types = (object,)

    def enrich(self, context):
        return self.check(context.enrich(self.data))

    def check(self, value):
        return isinstance(value, self.requisite_type)


class IsBoolean(_BaseIsType):
    __doc__ = _BaseIsType.__doc__
    requisite_type = bool


class IsDict(_BaseIsType):
    __doc__ = _BaseIsType.__doc__
    requisite_type = dict


class IsInteger(_BaseIsType):
    __doc__ = _BaseIsType.__doc__
    requisite_type = int

    def check(self, value):
        # Special case: True and False are integers as far as
        # Python is concerned.
        if value is True or value is False:
            return False
        return super().check(value)


class IsList(_BaseIsType):
    __doc__ = _BaseIsType.__doc__
    requisite_type = list


class IsNumber(IsInteger):
    __doc__ = _BaseIsType.__doc__
    requisite_type = Number


class IsString(_BaseIsType):
    __doc__ = _BaseIsType.__doc__
    requisite_type = str


class IsNone(_BaseIsType):
    """
    arguments: Data to typecheck.
    example: "`!{name} ...`"
    description: Returns True if the value enriched is None (null) or Void, False otherwise.
    """

    def check(self, value):
        return (value is None or value is Void)
