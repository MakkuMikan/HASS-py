import yaml
from dataclasses import dataclass


yaml.Dumper.ignore_aliases = lambda *args : True
yaml.emitter.Emitter.prepare_tag = lambda *args : ''


class Dumper(yaml.Dumper):
    def increase_indent(self, flow = False, indentless = False):
        return super(Dumper, self).increase_indent(flow, False)


class YAMLClass(type):
    def __new__(cls, name, bases, dct):
        dct['__yaml_tag__'] = f'!{name}'
        return super(YAMLClass, cls).__new__(cls, name, bases, dct)


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


class Data(YAMLObject):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def to_dict(self):
        return self.kwargs


class Time(YAMLObject):
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds


def filter_kwargs(kwargs):
    out = {}
    for key, value in kwargs.items():
        if isinstance(value, YAMLObject):
            out[key] = value.to_dict()
        else:
            out[key] = value
    return out