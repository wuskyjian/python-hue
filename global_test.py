import thread
import test
import global_events as events

print(events)

name = events.get_value('name')
score = events.get_value('score')

print("%s: %s" % (name, score))
