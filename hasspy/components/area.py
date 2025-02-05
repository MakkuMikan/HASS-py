from components.core import YAMLObject


class Area(YAMLObject):
    def __init__(self, id: str):
        self.area_id = id