from hasspy.components.core import YAMLObject


class Target(YAMLObject):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @staticmethod
    def Entity(id: str):
        return Target(entity_id=id)
    
    @staticmethod
    def Area(id: str):
        return Target(area_id=id)
    
    def to_dict(self):
        return self.kwargs


class Entity(Target):
    entity_id: str

    def __init__(self, id: str):
        super().__init__(entity_id=id)


class Area(Target):
    area_id: str

    def __init__(self, id: str):
        super().__init__(area_id=id)