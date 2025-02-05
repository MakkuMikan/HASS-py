from components.core import YAMLObject


class Condition(YAMLObject):
    def __init__(self, condition: str, **kwargs):
        self.condition = condition
        self.kwargs = kwargs

    @staticmethod
    def Template(value_template: str):
        return Condition('template', value_template=value_template)
    
    @staticmethod
    def Zone(entity_id: str, zone: str):
        return Condition('zone', entity_id=entity_id, zone=zone)
    
    def to_dict(self):
        return {
            'condition': self.condition,
            **self.kwargs
        }