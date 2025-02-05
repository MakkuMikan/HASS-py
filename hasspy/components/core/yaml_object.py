from dataclasses import dataclass
from components.core import YAMLClass


@dataclass
class YAMLObject(metaclass=YAMLClass):
    def to_dict(self):
        return self.__dict__
    
    @staticmethod
    def from_dict(d: dict):
        cls_name = d.pop('__yaml_tag__', None)
        if cls_name:
            cls_name = cls_name.lstrip('!')
            for subclass in YAMLObject.__subclasses__():
                if subclass.__name__ == cls_name:
                    return subclass(**d)
        return YAMLObject(**d)