from ..void import Void as VoidObj
from .base import BaseTag


class Void(BaseTag):
    value_types = (object,)
    def enrich(self, context):
        return VoidObj
