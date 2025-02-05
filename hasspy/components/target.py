from components.core import YAMLObject


class Target(YAMLObject):
    @staticmethod
    def Entity(id: str):
        return Target(entity_id=id)