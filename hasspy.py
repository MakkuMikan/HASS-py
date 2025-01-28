import yaml

yaml.Dumper.ignore_aliases = lambda *args : True
yaml.emitter.Emitter.prepare_tag = lambda *args : ''

class Dumper(yaml.Dumper):
    def increase_indent(self, flow = False, indentless = False):
        return super(Dumper, self).increase_indent(flow, False)

class YAMLClass(type):
    def __new__(cls, name, bases, dct):
        dct['__yaml_tag__'] = f'!{name}'
        return super(YAMLClass, cls).__new__(cls, name, bases, dct)

class YAMLObject(metaclass=YAMLClass):
    def to_dict(self):
        return self.__dict__
    
    @staticmethod
    def from_dict(d: dict):
        cls_name = d.pop('__yaml_tag__', None)
        if cls_name:
            cls_name = cls_name.lstrip('!')
            for subclass in YAMLObject.__subclasses__():
                if subclass.__name__ == cls_name:
                    return subclass(**d)
        return YAMLObject(**d)
    
class Data(YAMLObject):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def to_dict(self):
        return self.kwargs
    
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

        
class Actions(list[Action], YAMLObject):
    def __init__(self, *actions: Action):
        self.extend(actions)

    def to_dict(self):
        return [action.to_dict() for action in self]
    
    @staticmethod
    def from_dict(d: dict):
        return Actions([Action.from_dict(action) for action in d])

class Condition(YAMLObject):
    def __init__(self, condition: str, **kwargs):
        self.condition = condition
        self.kwargs = kwargs

    @staticmethod
    def Template(value_template: str):
        return Condition('template', value_template=value_template)
    
    def to_dict(self):
        return {
            'condition': self.condition,
            **self.kwargs
        }
    
class Conditions(list[Condition], YAMLObject):
    def __init__(self, *conditions):
        self.extend(conditions)

    def to_dict(self):
        return [condition.to_dict() for condition in self]
    
    @staticmethod
    def from_dict(d: dict):
        return Conditions([Condition.from_dict(condition) for condition in d])

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

class Time(YAMLObject):
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

class Trigger(YAMLObject):
    def __init__(self, trigger: str, **kwargs):
        self.trigger = trigger
        self.kwargs = kwargs

    @staticmethod
    def Time(at: str):
        return Trigger('time', at=at)
    
    @staticmethod
    def Calendar(entity_id: str, event: str, offset: str):
        return Trigger('calendar', entity_id=entity_id, event=event, offset=offset)
    
    def to_dict(self):
        return {
            'trigger': self.trigger,
            **self.kwargs
        }

class Wait(YAMLObject):
    def __init__(self, *triggers: Trigger, timeout: Time = None, continue_on_timeout: bool = False):
        self.triggers = triggers
        if timeout is not None:
            self.timeout = timeout
        self.continue_on_timeout = continue_on_timeout

    def to_dict(self):
        d = {
            'wait_for_trigger': [trigger.to_dict() for trigger in self.triggers],
            'continue_on_timeout': self.continue_on_timeout
        }
        if hasattr(self, 'timeout'):
            d['timeout'] = self.timeout.to_dict()
        return d
    
    @staticmethod
    def from_dict(d: dict):
        dd = {
            'triggers': [Trigger.from_dict(trigger) for trigger in d['wait_for_trigger']],
            'continue_on_timeout': d['continue_on_timeout']
        }
        if 'timeout' in d:
            dd['timeout'] = Time.from_dict(d['timeout'])
        return Wait(**dd)

class Entity(YAMLObject):
    def __init__(self, id: str):
        self.entity_id = id

class Area(YAMLObject):
    def __init__(self, id: str):
        self.area_id = id

class Automation(YAMLObject):
    def __init__(self, alias: str, description: str = '', mode: str = 'single', triggers: list[Trigger] = [], conditions: Conditions = [], actions: Actions = []):
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
            'triggers': [Trigger.from_dict(trigger) for trigger in d['triggers']],
            'conditions': [Conditions.from_dict(d['conditions'])],
            'actions': Actions.from_dict(d['actions'])
        }
        for key in d:
            if key not in ['triggers', 'conditions', 'actions']:
                dd[key] = d[key]
        return Automation(**dd)
    
    def __str__(self):
        return self.to_yaml()