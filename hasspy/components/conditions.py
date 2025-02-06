from hasspy.components.actions import Action, Actions
from hasspy.components.core import YAMLObject, filter_kwargs


class Condition(YAMLObject):
    def __init__(self, condition: str, **kwargs):
        self.condition = condition
        self.kwargs = kwargs

    @staticmethod
    def And(*conditions, **kwargs):
        return Condition('and', conditions=conditions[0] if isinstance(conditions[0], Conditions) else Conditions(*conditions), **kwargs)
    
    @staticmethod
    def Or(*conditions, **kwargs):
        return Condition('or', conditions=conditions[0] if isinstance(conditions[0], Conditions) else Conditions(*conditions), **kwargs)
    
    @staticmethod
    def State(entity_id: str, state: str, **kwargs):
        return Condition('state', entity_id=entity_id, state=state, **kwargs)
    
    @staticmethod
    def StateAttribute(entity_id: str, attribute: str, state: str, **kwargs):
        return Condition('state', entity_id=entity_id, attribute=attribute, state=state, **kwargs)

    @staticmethod
    def Template(value_template: str, **kwargs):
        return Condition('template', value_template=value_template, **kwargs)
    
    @staticmethod
    def Trigger(ids: str | list[str], **kwargs):
        return Condition('trigger', id=ids if isinstance(ids, list) else [ids], **kwargs)
    
    @staticmethod
    def Zone(entity_id: str, zone: str, **kwargs):
        return Condition('zone', entity_id=entity_id, zone=zone, **kwargs)
    
    def to_dict(self):
        return {
            'condition': self.condition,
            **filter_kwargs(self.kwargs)
        }


class Conditions(YAMLObject):
    def __init__(self, *conditions: Condition):
        self.conditions = conditions

    def to_dict(self):
        return [condition.to_dict() for condition in self.conditions]
    
    @staticmethod
    def from_dict(d: dict):
        return Conditions([Condition.from_dict(condition) for condition in d])


class If(YAMLObject):
    def __init__(self, *conditions: Conditions | Condition):
        self.conditions = conditions[0] if isinstance(conditions[0], Conditions) else Conditions(*conditions)

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
        d =  {
            'if': self.conditions.to_dict()
        }
        if hasattr(self, 'then'):
            d['then'] = self.then.to_dict()
        if hasattr(self, 'else_'):
            d['else'] = self.else_.to_dict()
        return d


class Choice(YAMLObject):
    def __init__(self, conditions: Condition | Conditions, *sequence: Action | Actions, **kwargs):
        self.conditions = conditions if isinstance(conditions, Conditions) else Conditions(conditions)
        self.sequence = sequence[0] if isinstance(sequence[0], Actions) else Actions(*sequence)
        self.kwargs = kwargs

    @staticmethod
    def State(entity_id: str, state: str, *sequence: Action | Actions, **kwargs):
        return Choice(Condition.State(entity_id, state), *sequence, **kwargs)
    
    @staticmethod
    def StateAttribute(entity_id: str, attribute: str, state: str, *sequence: Action | Actions, **kwargs):
        return Choice(Condition.StateAttribute(entity_id, attribute, state), *sequence, **kwargs)

    @staticmethod
    def Template(value_template: str, *sequence: Action | Actions, **kwargs):
        return Choice(Condition.Template(value_template), *sequence, **kwargs)

    def to_dict(self):
        return {
            'conditions': self.conditions.to_dict(),
            'sequence': self.sequence.to_dict(),
            **filter_kwargs(self.kwargs)
        }
    
    @staticmethod
    def from_dict(d: dict):
        dd = {
            'conditions': Conditions.from_dict(d['conditions']),
            'sequence': [Action.from_dict(action) for action in d['sequence']]
        }
        for key in d:
            if key not in ['conditions', 'sequence']:
                dd[key] = d[key]
        return Choice(**dd)
    
    def with_alias(self, alias: str):
        self.alias = alias
        return self


class Choose(YAMLObject):
    def __init__(self, *choices: Choice, default: Action | Actions = None, **kwargs):
        self.choices = choices
        if default is not None:
            self.default = default if isinstance(default, Actions) else Actions(default)
        self.kwargs = kwargs

    def to_dict(self):
        d = {
            'choose': [choice.to_dict() for choice in self.choices],
            **filter_kwargs(self.kwargs)
        }
        if hasattr(self, 'default'):
            d['default'] = self.default.to_dict()
        return d
    
    @staticmethod
    def from_dict(d: dict):
        return Choose([Choice.from_dict(choice) for choice in d])


class And(Condition):
    def __init__(self, *conditions: Conditions | Condition):
        super().__init__('and')
        self.conditions = conditions[0] if isinstance(conditions[0], Conditions) else Conditions(*conditions)

    def to_dict(self):
        return {
            'condition': self.condition,
            'conditions': self.conditions.to_dict()
        }
    
    @staticmethod
    def from_dict(d: dict):
        return And([Condition.from_dict(condition) for condition in d['conditions']])


class Or(Condition):
    def __init__(self, *conditions: Conditions | Condition):
        super().__init__('or')
        self.conditions = conditions[0] if isinstance(conditions[0], Conditions) else Conditions(*conditions)

    def to_dict(self):
        return {
            'condition': self.condition,
            'conditions': self.conditions.to_dict()
        }
    
    @staticmethod
    def from_dict(d: dict):
        return Or([Condition.from_dict(condition) for condition in d['conditions']])