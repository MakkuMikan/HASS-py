from hasspy import Automation, Action, Actions, Condition, Choose, Choice, Wait, Trigger, Variables, Time, Entity, Area, Parallel, Data

wake_up = Automation(
    alias='Wake Up',
    triggers=[Trigger.Time('06:00:00')],
    actions=Actions(
        Action('calendar.get_events', data=Data(duration=Time(hours=10)), target=Entity(
            'calendar.work'), response_variable='get_events_response'),
        Condition.Template(
            "{{ get_events_response['calendar.work'].events | count > 0 }}"),
        Variables(
            next_work="{{ get_events_response['calendar.work'].events.0 }}",
            fade_duration=Time(hours=1),
            after_complete='Turn Off'
        ),
        # Maybe implement a builder for templates like this?
        Wait(Trigger.Time(
            "{{ (next_work.start | as_datetime - timedelta(hours=fade_duration.hours, minutes=fade_duration.minutes, seconds=fade_duration.seconds)).time() }}"), timeout=Time(hours=10), continue_on_timeout=False),
        Choose(
            Choice.Template("{{ next_work.location == 'Office' }}", Variables(
                fade_duration=Time(hours=1),
                after_complete='Turn Off'
            )),
            Choice.Template("{{ next_work.location == 'Home' }}", Variables(
                fade_duration=Time(minutes=30),
                after_complete='Working from Home'
            ))
        ),
        Action('light.turn_on', data=Data(kelvin=2000,
               brightness_pct=1), target=Area('jack_s_bedroom')),
        Parallel(
            Action('script.light_fade', data=Data(
                lampBrightnessScale='zeroToTwoFiftyFive',
                easingTypeInput='auto',
                endBrightnessPercent=100,
                endBrightnessEntityScale='zeroToOneHundred',
                autoCancelThreshold=10,
                shouldStopIfTheLampIsTurnedOffDuringTheFade=True,
                shouldResetTheStopEntityToOffAtStart=False,
                shouldInvertTheValueOfTheStopEntity=False,
                minimumStepDelayInMilliseconds=100,
                shouldTryToUseNativeLampTransitionsToo=True,
                isDebugMode=False,
                light='light.wiz_rgbw_tunable_2278da',
                endColorTemperatureKelvin=6500,
                transitionTime="{{ fade_duration }}")),
            Action('script.light_fade', data=Data(
                lampBrightnessScale='zeroToTwoFiftyFive',
                easingTypeInput='auto',
                endBrightnessPercent=100,
                endBrightnessEntityScale='zeroToOneHundred',
                autoCancelThreshold=10,
                shouldStopIfTheLampIsTurnedOffDuringTheFade=True,
                shouldResetTheStopEntityToOffAtStart=False,
                shouldInvertTheValueOfTheStopEntity=False,
                minimumStepDelayInMilliseconds=100,
                shouldTryToUseNativeLampTransitionsToo=True,
                isDebugMode=False,
                light='light.wiz_rgbw_tunable_08365a',
                endColorTemperatureKelvin=6500,
                transitionTime="{{ fade_duration }}"))
        ),
        Wait(Trigger.Calendar('calendar.work', event='start',
             offset='0:0:0'), timeout=Time(hours=1)),
        Choose(
            Choice.Template("{{ after_complete == 'Turn Off' }}", Action(
                'light.turn_off', target=Area('jack_s_bedroom'))),
            Choice.Template("{{ after_complete == 'Working from Home' }}", Action(
                'scene.turn_on', target=Entity(id='scene.working_from_home')))
        )
    )
)

with open('wake-up.yaml', 'w+') as f:
    f.write(wake_up.to_yaml())