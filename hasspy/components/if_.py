from components import Action, Actions, Condition, Conditions
from components.core import YAMLObject


class If(YAMLObject):
    def __init__(self, *conditions: Conditions | Condition):
        self.conditions = conditions[0] if len(conditions) == 1 else Conditions(*conditions)

    @staticmethod
    def Condition(condition: str, **kwargs):
        return If(Condition(condition, **kwargs))

    @staticmethod
    def Zone(entity_id: str, zone: str):
        return If(Condition.Zone(entity_id, zone))

    def Then(self, *actions: Action | Actions):
        self.then = actions[0] if len(actions) == 1 else Actions(*actions)
        return self
    
    def Else(self, *actions: Action | Actions):
        self.else_ = actions[0] if len(actions) == 1 else Actions(*actions)
        return self
    
    def to_dict(self):
        return {
            'if': self.conditions.to_dict(),
            'then': self.then.to_dict(),
            'else': self.else_.to_dict()
        }