from components import Actions, Condition, Conditions
from components.core import YAMLObject


class Choice(YAMLObject):
    def __init__(self, conditions: Condition | Conditions, sequence: Actions, **kwargs):
        self.conditions = conditions if isinstance(conditions, Conditions) else Conditions(conditions)
        self.sequence = sequence if isinstance(sequence, Actions) else Actions(*sequence)
        self.kwargs = kwargs

    @staticmethod
    def Template(value_template: str, *sequence, **kwargs):
        return Choice(Condition.Template(value_template), sequence, **kwargs)

    def to_dict(self):
        return {
            'conditions': self.conditions.to_dict(),
            'sequence': self.sequence.to_dict(),
            **self.kwargs
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