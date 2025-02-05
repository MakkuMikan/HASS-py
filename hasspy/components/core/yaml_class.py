class YAMLClass(type):
    def __new__(cls, name, bases, dct):
        dct['__yaml_tag__'] = f'!{name}'
        return super(YAMLClass, cls).__new__(cls, name, bases, dct)