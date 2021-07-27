from numbers import Number
from typing import Optional, Tuple, Type, Union

from ..context import Context
from ..void import Void, VoidType
from .base import BaseTag


class _BaseIsType(BaseTag):
    """
    arguments: Data to typecheck.
    example: "`!{name} ...`"
    description: Returns True if the value enriched is of the given type, False otherwise.
    """

    requisite_type: Union[Type, Tuple[Type, ...]]
    value_types = (object,)

    def enrich(self, context: Context) -> bool:
        return self.check(context.enrich(self.data))

    def check(self, value) -> bool:
        return isinstance(value, self.requisite_type)


class IsBoolean(_BaseIsType):
    __doc__ = _BaseIsType.__doc__
    requisite_type = bool


class IsDict(_BaseIsType):
    __doc__ = _BaseIsType.__doc__
    requisite_type = dict


class IsInteger(_BaseIsType):
    __doc__ = _BaseIsType.__doc__
    requisite_type: Type = int

    def check(self, value: Union[int, float, bool]) -> bool:
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

    def check(self, value: Optional[Union[VoidType, str]]) -> bool:
        return value is None or value is Void
