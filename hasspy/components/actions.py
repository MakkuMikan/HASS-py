from hasspy.components.core import Data, Time, YAMLObject
from hasspy.components.targets import Entity, Target


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


class Actions(YAMLObject):
    def __init__(self, *actions: Action):
        self.actions = actions

    def to_dict(self):
        return [action.to_dict() for action in self.actions]
    
    @staticmethod
    def from_dict(d: dict):
        return Actions([Action.from_dict(action) for action in d])


class Calendar:
    @staticmethod
    def get_events(target: Target, start: str = None, end: str = None, duration: Time = None, response_variable: str = None, **kwargs):
        raw_data = {}
        if start is not None:
            raw_data['start_date_time'] = start
        if end is not None:
            raw_data['end_date_time'] = end
        if duration is not None:
            raw_data['duration'] = duration.to_dict()
        return Action(
            'calendar.get_events',
            data=Data(**raw_data),
            target=target,
            response_variable=response_variable,
            **kwargs
        )


class Variables(YAMLObject):
    def __init__(self, **variables):
        self.variables = variables

    def to_dict(self):
        return {
            'variables': self.variables
        }


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