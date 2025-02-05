from components import Action, Data, Target, Time


class Calendar(Action):
    @staticmethod
    def get_events(duration: Time, target: Target):
        return Calendar('calendar.get_events', data=Data(duration=duration))