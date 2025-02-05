from components.core import YAMLObject


class Variables(YAMLObject):
    def __init__(self, **variables):
        self.variables = variables

    def to_dict(self):
        return {
            'variables': self.variables
        }