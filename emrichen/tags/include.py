import base64
import glob
import os
from typing import TextIO

from ..context import Context
from ..template import Template
from ..void import Void
from .base import BaseTag


class _BaseInclude(BaseTag):
    def _open_file(self, context: Context, mode: str = 'r') -> TextIO:
        return open(self._absolve_path(context, self.data), mode)

    def _absolve_path(self, context: Context, path: str):
        # Named humorously for humor's sake.
        return os.path.join(
            os.path.dirname(context['__file__']), path)


class Include(_BaseInclude):
    """
    arguments: Path to a template to include
    example: "`!Include ../foo.yml`"
    description: Renders the requested template at this location. Both absolute and relative paths work.
    """

    def get_template(self, context: Context) -> Template:
        from ..template import Template

        with self._open_file(context) as include_file:
            return Template.parse(include_file)

    def enrich(self, context: Context):
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

    def get_data(self, context: Context) -> bytes:
        with self._open_file(context, 'rb') as include_file:
            return include_file.read()

    def enrich(self, context: Context) -> str:
        return self.get_data(context).decode('UTF-8')


class IncludeBase64(IncludeText):
    """
    arguments: Path to a binary file
    example: "`!IncludeBase64 ../foo.pdf`"
    description: Loads the given binary file and returns the contents encoded as Base64.
    """

    def enrich(self, context: Context) -> str:
        data = super().get_data(context)
        return base64.b64encode(data).decode('UTF-8')


class IncludeBinary(IncludeText):
    """
    arguments: Path to a binary file
    example: "`!IncludeBinary ../foo.pdf`"
    description: Loads the given binary file and returns the contents as bytes.  This is practically only useful for hashing.
    """

    def enrich(self, context: Context) -> bytes:
        return super().get_data(context)


class IncludeGlob(_BaseInclude):
    """
    arguments: A string (or a list thereof) of glob patterns of templates to include
    example: "`!IncludeGlob bits/**.in.yml`"
    description: |
      Expands the glob patterns and renders all templates into a list.
      YAML files that contain more than one document will have all of those templates rendered into
      the same flat list.
      Expansion results are lexicographically sorted.
      As with Python's `glob.glob()`, use a double star (`**`) for recursion.
    """
    value_types = (list, str)

    def enrich(self, context: Context):
        from ..template import Template

        # Ensure input data is a list.
        data = self.data
        if not isinstance(data, list):
            data = [data]

        output = []
        for item in data:
            pattern = context.enrich(item)
            if not isinstance(pattern, str):
                raise TypeError('Pattern {!r} in IncludeGlob is not a string'.format(pattern))
            pattern = self._absolve_path(context, pattern)
            names = sorted(glob.glob(pattern, recursive=True))
            for name in names:
                if not os.path.isfile(name):
                    continue
                with open(name) as include_file:
                    template = Template.parse(include_file)
                output.extend(template.enrich(context))

        return output
