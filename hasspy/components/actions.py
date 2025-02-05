from components import Action
from components.core import YAMLObject


class Actions(list[Action], YAMLObject):
    def __init__(self, *actions: Action):
        self.extend(actions)

    def to_dict(self):
        return [action.to_dict() for action in self]
    
    @staticmethod
    def from_dict(d: dict):
        return Actions([Action.from_dict(action) for action in d])