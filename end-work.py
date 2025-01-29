from hasspy import Automation, Action, Actions, Condition, Choose, Choice, Wait, Trigger, Variables, Time, Entity, Area, Parallel, Data

end_work = Automation(
    alias='End Work',
    triggers=[Trigger.Zone.Leave('zone.work', 'person.jack'), Trigger.State())],