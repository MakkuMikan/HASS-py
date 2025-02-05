from components import Action, Actions
from components.core import YAMLObject


class Parallel(YAMLObject):
    def __init__(self, *actions: Actions | Action):
        self.actions = actions[0] if isinstance(actions[0], Actions) else Actions(*actions)

    def to_dict(self):
        return {
            'parallel': self.actions.to_dict()
        }
    
    @staticmethod
    def from_dict(d: dict):
        return Parallel(Actions.from_dict(d['parallel']))