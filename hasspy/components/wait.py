from components import Entity, Time, Trigger
from components.core import YAMLObject


class Wait(YAMLObject):
    def __init__(self, *triggers: Trigger, timeout: Time = None, continue_on_timeout: bool = False):
        self.triggers = triggers
        if timeout is not None:
            self.timeout = timeout
        self.continue_on_timeout = continue_on_timeout

    class Zone:
        @staticmethod
        def Enter(zone: str, entity_id: str, **kwargs):
            return Wait(Trigger.Zone.Enter(zone, entity_id), **kwargs)
        
        @staticmethod
        def Leave(zone: str, entity_id: str, **kwargs):
            return Wait(Trigger.Zone.Leave(zone, entity_id), **kwargs)

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