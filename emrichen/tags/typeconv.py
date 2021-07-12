from numbers import Number
from collections.abc import Mapping
from typing import Optional, Type, Union

from ..context import Context
from ..void import Void, VoidType
from .base import BaseTag


class _BaseToType(BaseTag):
    """
    arguments: Data to convert.
    example: "`!{name} ...`"
    description: Converts the input to the desired type.
    """

    value_types = (object,)
    target_type: Type

    def enrich(self, context: Context):
        return self.target_type(context.enrich(self.data))


class ToBoolean(_BaseToType):
    __doc__ = _BaseToType.__doc__
    target_type = bool


class ToInteger(_BaseToType):
    """
    arguments: Either single argument containing the data to convert, or an object with `value:` and `radix:`.
    example: `!ToInteger "50"`, `!ToInteger value: "C0FFEE", radix: 16`
    description: Converts the input to Python `int`. Radix is never inferred from input: if not supplied, it is always 10.
    """

    target_type = int

    def enrich(self, context: Context):
        data = context.enrich(self.data)

        if isinstance(data, Mapping):
            value = data["value"]
            radix = data.get("radix", 10)
            return self.target_type(value, radix)
        else:
            return self.target_type(data)


class ToFloat(_BaseToType):
    __doc__ = _BaseToType.__doc__
    target_type = float


class ToString(_BaseToType):
    __doc__ = _BaseToType.__doc__
    target_type = str
