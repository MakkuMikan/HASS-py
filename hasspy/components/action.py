from components import Data, Entity
from components.core import YAMLObject


class Action(YAMLObject):
    def __init__(self, action: str, metadata: YAMLObject = Data(), data: YAMLObject = Data(), target: YAMLObject = None, response_variable: str = None):
        self.action = action
        self.metadata = metadata
        self.data = data
        if target is not None:
            self.target = target
        if response_variable is not None:
            self.response_variable = response_variable

    def to_dict(self):
        d = {
            'action': self.action,
            'metadata': self.metadata.to_dict() if self.metadata else None,
            'data': self.data.to_dict() if self.data else None,
        }
        if hasattr(self, 'target'):
            d['target'] = self.target.to_dict()
        if hasattr(self, 'response_variable'):
            d['response_variable'] = self.response_variable
        return d
    
    @staticmethod
    def from_dict(d: dict):
        dd = {
            'action': d['action']
        }
        if 'metadata' in d:
            dd['metadata'] = Data.from_dict(**d['metadata'])
        if 'data' in d:
            dd['data'] = Data.from_dict(**d['data'])
        if 'target' in d:
            dd['target'] = Entity.from_dict(**d['target'])
        if 'response_variable' in d:
            dd['response_variable'] = d['response_variable']
        return Action(**dd)