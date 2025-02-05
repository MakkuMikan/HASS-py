import yaml


yaml.Dumper.ignore_aliases = lambda *args : True
yaml.emitter.Emitter.prepare_tag = lambda *args : ''

class Dumper(yaml.Dumper):
    def increase_indent(self, flow = False, indentless = False):
        return super(Dumper, self).increase_indent(flow, False)