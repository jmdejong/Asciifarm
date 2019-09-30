
from ..system import System
from ..datacomponents import Events

@System([Events])
def handleevents(obj, roomData, events):
    while True:
        try:
            event, args, kwargs = events.messages.popleft()
        except IndexError:
            break
        for listener in list(obj.listeners[event]):
            listener(obj, *args, **kwargs)
    
    roomData.removeComponent(obj, Events)
