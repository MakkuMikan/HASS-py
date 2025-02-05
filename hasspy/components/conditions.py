from components import Condition
from components.core import YAMLObject


class Conditions(list[Condition], YAMLObject):
    def __init__(self, *conditions):
        self.extend(conditions)

    def to_dict(self):
        return [condition.to_dict() for condition in self]
    
    @staticmethod
    def from_dict(d: dict):
        return Conditions([Condition.from_dict(condition) for condition in d])