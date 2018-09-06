from ..exceptions import NoSuchTag
from ..tags.base import tag_registry


def make_compose(names, value):
    if isinstance(names, str):
        names = [name.strip() for name in names.split(',')]
    for name in names:
        if name not in tag_registry:
            raise NoSuchTag(name)
    data = {'value': value, 'tags': names}
    return tag_registry['Compose'](data)
