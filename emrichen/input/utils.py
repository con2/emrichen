from typing import TYPE_CHECKING, Any, List, Union

from ..exceptions import NoSuchTag
from ..tags.base import tag_registry

if TYPE_CHECKING:
    from ..tags.compose import Compose


def make_compose(names: Union[str, List[str]], value: Any) -> 'Compose':
    if isinstance(names, str):
        names = [name.strip() for name in names.split(',')]
    for name in names:
        if name not in tag_registry:
            raise NoSuchTag(name)
    data = {'value': value, 'tags': names}
    return tag_registry['Compose'](data)
