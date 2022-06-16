# snippets/prefilter.py
from typing import Any, Dict

# Simple Conditions
EQUALS = "Equals"
GREATER_THAN_EQUAL = 'GreaterThanOrEqual'
LESS_THAN_EQUAL = 'LessThanOrEqual'
LESS_THAN = 'LessThan'
GREATER_THAN = 'GreaterThan'
CONTAINS = 'Contains'
IN = 'In'

# Combo Conditions
NOT = "Not"
AND = "And"
OR = "Or"

class PreFilter:
    key: str
    condition: str
    value: Any

    def __init__(self, config: Dict):
        self.Not = []
        self.Or = []
        self.And = []

        self.key = config.get('key')
        self.condition = config.get('condition')
        self.value = config.get('value', '')

        for i in config.get(NOT, []):
            self.Not.append(PreFilter(i))
        for i in config.get(AND, []):
            self.And.append(PreFilter(i))
        for i in config.get(OR, []):
            self.Or.append(PreFilter(i))

        self._compiledFilter = self.__compile()

    def contains(self, event):
        return self.value in event.get(self.key)

    def _in(self, event):
        return event.get(self.key) in self.value

    def eq(self, event):
        return event.get(self.key) == self.value

    def gt(self, event):
        return event.get(self.key) > self.value

    def gte(self, event):
        return event.get(self.key) >= self.value

    def lt(self, event):
        return event.get(self.key) < self.value

    def lte(self, event):
        return event.get(self.key) <= self.value

    def __compile(self):
        if self.key is not None:
            opts = {
                EQUALS: self.eq,
                GREATER_THAN_EQUAL: self.gte,
                LESS_THAN_EQUAL: self.lte,
                LESS_THAN: self.lt,
                GREATER_THAN: self.gt,
                CONTAINS: self.contains,
                IN: self._in,
            }

            fn = opts.get(self.condition, None)
            if fn is None:
                return lambda ev: False

            return fn
        if len(self.Or) > 0:
            def _or(event):
                for f in self.Or:
                    if f.filter(event):
                        return True
                return False

            return _or

        if len(self.And) > 0:
            def _and(event):
                for f in self.And:
                    if f.filter(event) is False:
                        return False
                return True

            return _and

        if len(self.Not) > 0:
            def _not(event):
                bools: [bool] = []
                for f in self.Not:
                    bools.append(f.filter(event))

                return not (all(bools))

            return _not

        return lambda x: False

    def filter(self, event) -> bool:
        return self._compiledFilter(event)
