from components import Choice
from components.core import YAMLObject


class Choose(list[Choice], YAMLObject):
    def __init__(self, *choices: Choice):
        self.extend(choices)

    def to_dict(self):
        return {
            'choose': [choice.to_dict() for choice in self]
        }
    
    @staticmethod
    def from_dict(d: dict):
        return Choose([Choice.from_dict(choice) for choice in d])