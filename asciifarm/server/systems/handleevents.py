
from ..system import system
from ..datacomponents import Events

@system([Events])
def handleevents(obj, roomData, events):
    while True:
        try:
            event, args, kwargs = events.messages.popleft()
        except IndexError:
            break
        for listener in list(obj.listeners[event]):
            listener(obj, *args, **kwargs)
    
    roomData.removeComponent(obj, events)
