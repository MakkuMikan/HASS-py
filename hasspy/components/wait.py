from hasspy.components.core import Time, YAMLObject
from hasspy.components.triggers import Trigger, Triggers


class Wait(YAMLObject):
    def __init__(self, *triggers: Trigger | Triggers, timeout: Time = None, continue_on_timeout: bool = False):
        self.triggers = triggers[0] if isinstance(triggers[0], Triggers) else triggers
        if timeout is not None:
            self.timeout = timeout
        self.continue_on_timeout = continue_on_timeout

    def Time(at: str, **kwargs):
        return Wait(Trigger.Time(at), **kwargs)

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


class Delay(Time):
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        super().__init__(hours, minutes, seconds)

    def to_dict(self):
        return {
            'delay': super().to_dict()
        }