from hasspy.components.core import YAMLObject


class Trigger(YAMLObject):
    trigger: str

    def __init__(self, trigger: str, **kwargs):
        self.trigger = trigger
        self.kwargs = {x: y for x, y in kwargs.items() if x not in ['from_']}
        if 'from_' in kwargs:
            self.kwargs['from'] = kwargs['from_']
    
    @staticmethod
    def Calendar(entity_id: str, event: str, offset: str, **kwargs):
        return Trigger('calendar', entity_id=entity_id, event=event, offset=offset, **kwargs)

    @staticmethod
    def Time(at: str, **kwargs):
        return Trigger('time', at=at, **kwargs)
    
    @staticmethod
    def State(entity_id: str | list[str], from_: str, to: str, **kwargs):
        return Trigger('state', entity_id=entity_id if isinstance(entity_id, list) else [entity_id], from_=from_, to=to, **kwargs)
    
    class Zone:
        @staticmethod
        def Enter(zone: str, entity_id: str, **kwargs):
            return Trigger('zone', zone=zone, entity_id=entity_id, event='enter', **kwargs)
        
        @staticmethod
        def Leave(zone: str, entity_id: str, **kwargs):
            return Trigger('zone', zone=zone, entity_id=entity_id, event='leave', **kwargs)
    
    def to_dict(self):
        return {
            'trigger': self.trigger,
            **self.kwargs
        }


class Triggers(YAMLObject):
    def __init__(self, *triggers: Trigger):
        self.triggers = triggers

    def to_dict(self):
        return [trigger.to_dict() for trigger in self.triggers]
    
    @staticmethod
    def from_dict(d: dict):
        return Triggers([Trigger.from_dict(trigger) for trigger in d])