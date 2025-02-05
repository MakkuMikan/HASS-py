from components.core import YAMLObject


class Data(YAMLObject):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def to_dict(self):
        return self.kwargs