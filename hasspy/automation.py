import yaml
from hasspy.components.actions import Actions
from hasspy.components.conditions import Conditions
from hasspy.components.core import YAMLObject
from hasspy.components.core import Dumper
from hasspy.components.triggers import Triggers


class Automation(YAMLObject):
    def __init__(self, alias: str, description: str = '', mode: str = 'single', triggers: Triggers = [], conditions: Conditions = [], actions: Actions = []):
        self.alias = alias
        self.description = description
        self.mode = mode
        self.triggers = triggers
        self.conditions = conditions
        self.actions = actions
    
    def to_dict(self):
        return {
            'alias': self.alias,
            'description': self.description,
            'triggers': [trigger.to_dict() for trigger in self.triggers],
            'conditions': [condition.to_dict() for condition in self.conditions],
            'actions': self.actions.to_dict(),
            'mode': self.mode
        }
    
    def to_yaml(self):
        return yaml.dump(self.to_dict(), sort_keys=False, Dumper=Dumper, width=1000)
    
    @staticmethod
    def from_yaml(yaml_str: str):
        return yaml.load(yaml_str)
    
    @staticmethod
    def from_dict(d: dict):
        dd = {
            'triggers': Triggers.from_dict(d['triggers']),
            'conditions': Conditions.from_dict(d['conditions']),
            'actions': Actions.from_dict(d['actions'])
        }
        for key in d:
            if key not in ['triggers', 'conditions', 'actions']:
                dd[key] = d[key]
        return Automation(**dd)
    
    def __str__(self):
        return self.to_yaml()
    
    def write(self, path: str):
        with open(path, 'w+') as f:
            f.write(self.to_yaml())