from components import Target


class Entity(Target):
    entity_id: str

    def __init__(self, id: str):
        super().__init__(entity_id=id)