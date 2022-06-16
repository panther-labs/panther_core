#snippets
from typing import Dict

from .pre_filter import PreFilter


class Snippet:
    id: str
    type: str
    when: PreFilter

    def __init__(self, config: Dict):

        for each_field in ["id", "type"]:
            if not (each_field in config) or not isinstance(config[each_field], str):
                raise AssertionError('Field "%s" of type str is required field' % each_field)

        self.id = config['id']
        self.type = config['type']
        self.when = PreFilter(config.get('when', {}))

    def prefilter(self, event: Dict) -> bool:
        return self.when.filter(event)
