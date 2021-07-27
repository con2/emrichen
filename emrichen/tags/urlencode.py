from collections.abc import Mapping
from urllib.parse import parse_qsl, quote_plus, urlencode, urlparse, urlunparse

from ..context import Context
from .base import BaseTag


class URLEncode(BaseTag):
    """
    arguments: |
        A string to encode
        **OR**
        `url`: The URL to combine query parameters into
        `query`: An object of query string parameters to add OR a string of query string parameters
    example: |
        `!URLEncode "foo+bar"`
        `!URLEncode { url: "https://example.com/", query: { foo: bar } }`
    description:
        Encodes strings for safe inclusion in a URL, or combines query string parameters into a URL.
    ---
    Three modes of operation:

    1. Just encode a plain string

        !URLEncode "foo+bar" -> "foo%2Bbar"

    2. Form a query string

        !URLEncode
            query:
                foo: bar

        -> "foo=bar"

    3a. Combine a base URL and query string parameters

        !URLEncode
            url: "https://example.com/?foo=x"
            query:
                bar: xyzzy

        -> "https://example.com/?foo=x&bar=xyzzy"

    3b. Combine a base URL and query string parameters

        !URLEncode
            url: "https://example.com/?foo=x"
            query: "bar=xyzzy"

        -> "https://example.com/?foo=x&bar=xyzzy"

    TODO Add query_mode: append|replace (currently append)
    """

    value_types = (dict, str, BaseTag)

    def enrich(self, context: Context) -> str:
        if isinstance(self.data, Mapping):
            url = context.enrich(self.data.get('url'))
            query = context.enrich(self.data.get('query'))

            if isinstance(query, dict):
                query = list(query.items())
            elif isinstance(query, str):
                query = parse_qsl(query)

            if url is not None:  # empty string ok!
                if not isinstance(url, str):
                    raise TypeError(f"{self}: `url` {url!r} is not a string")
                # 3. Combine a base URL and query string parameters
                url = urlparse(url)
                query = parse_qsl(url.query) + (query or [])
                url = url._replace(query=urlencode(query))
                return urlunparse(url)

            elif query is not None:  # empty object ok!
                # 2. Form a query string
                return urlencode(query)

            else:
                raise TypeError(f'{self}: needs url, query or both')

        else:
            data = context.enrich(self.data)

            if isinstance(data, str):
                # 1. Just encode a plain string
                return quote_plus(data)

            else:
                raise TypeError(f'{self}: single argument must be a string (got {type(data)})')
