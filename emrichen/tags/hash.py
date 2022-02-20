import hashlib
from typing import Any

from ..context import Context
from .base import BaseTag


class _BaseHash(BaseTag):
    """
    arguments: Data to hash
    example: "`!{name} 'some data to hash'`"
    description: Hashes the given data using the {name} algorithm. If the data is not binary, it is converted to UTF-8 bytes.
    """

    value_types = (
        str,
        object,
    )

    hasher: Any = None  # TODO: what's the proper type for a hasher factory?

    def enrich(self, context: Context) -> str:
        data = context.enrich(self.data)
        if not isinstance(data, bytes):
            if not isinstance(data, str):
                data = str(data)
            data = data.encode('UTF-8')
        return self.hasher(data).hexdigest()


class MD5(_BaseHash):
    hasher = hashlib.md5
    __doc__ = _BaseHash.__doc__


class SHA1(_BaseHash):
    hasher = hashlib.sha1
    __doc__ = _BaseHash.__doc__


class SHA256(_BaseHash):
    hasher = hashlib.sha256
    __doc__ = _BaseHash.__doc__
