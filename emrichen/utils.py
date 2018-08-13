from .void import Void


def maybe_template(value, default=None):
    from .template import Template
    return (Template([value]) if value else default)


def maybe_enrich(context, value, first=False):
    if hasattr(value, 'enrich'):
        value = value.enrich(context)
        if first and isinstance(value, list):
            if value:
                return value[0]
            else:
                return Void
    return value


def get_first_key(dct, keys, default=None):
    for key in keys:
        if key in dct:
            return dct[key]
    return default
