from yaml import SafeLoader

from .tags.base import tag_registry


class RichLoader(SafeLoader):
    def __init__(self, stream):
        super(RichLoader, self).__init__(stream)
        self.add_tag_constructors()

    def add_tag_constructors(self):
        self.yaml_constructors = self.yaml_constructors.copy()  # Grab an instance copy from the class
        for name, tag in tag_registry.items():
            self.yaml_constructors[f'!{name}'] = tag.load
