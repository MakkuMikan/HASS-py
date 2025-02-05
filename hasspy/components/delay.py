from components import Time


class Delay(Time):
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        super().__init__(hours, minutes, seconds)

    def to_dict(self):
        return {
            'delay': super().to_dict()
        }