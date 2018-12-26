import base64
import os

from .base import BaseTag
from ..void import Void


class _BaseInclude(BaseTag):
    def _open_file(self, context, mode='r'):
        include_path = os.path.join(
            os.path.dirname(context['__file__']), self.data)

        return open(include_path, mode)


class Include(_BaseInclude):
    """
    arguments: Path to a template to include
    example: "`!Include ../foo.yml`"
    description: Renders the requested template at this location. Both absolute and relative paths work.
    """

    def get_template(self, context):
        from ..template import Template

        with self._open_file(context) as include_file:
            return Template.parse(include_file)

    def enrich(self, context):
        template = self.get_template(context)
        enriched = template.enrich(context)

        if len(enriched) == 0:
            return Void
        if len(enriched) > 1:
            raise ValueError('!Include can only include single-document templates')

        return enriched[0]


class IncludeText(_BaseInclude):
    """
    arguments: Path to an UTF-8 text file
    example: "`!IncludeText ../foo.toml`"
    description: Loads the given UTF-8 text file and returns the contents as a string.
    """

    def get_data(self, context) -> bytes:
        with self._open_file(context, 'rb') as include_file:
            return include_file.read()

    def enrich(self, context):
        return self.get_data(context).decode('UTF-8')


class IncludeBase64(IncludeText):
    """
    arguments: Path to a binary file
    example: "`!IncludeBase64 ../foo.pdf`"
    description: Loads the given binary file and returns the contents encoded as Base64.
    """

    def enrich(self, context):
        data = super().get_data(context)
        return base64.b64encode(data).decode('UTF-8')


class IncludeBinary(IncludeText):
    """
    arguments: Path to a binary file
    example: "`!IncludeBinary ../foo.pdf`"
    description: Loads the given binary file and returns the contents as bytes.  This is practically only useful for hashing.
    """

    def enrich(self, context):
        return super().get_data(context)
