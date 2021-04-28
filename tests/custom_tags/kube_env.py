from emrichen.tags.base import BaseTag


class KubeEnv(BaseTag):
    value_types = (dict,)

    def enrich(self, context):
        return [dict(name=name, value=str(value)) for name, value in context.enrich(self.data).items()]
