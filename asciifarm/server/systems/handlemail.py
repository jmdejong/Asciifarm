
from ..system import System
from ..datacomponents import Messages

@System(Messages)
def handlemail(obj, roomData, messages):
    while True:
        try:
            event, args, kwargs = messages.messages.popleft()
        except IndexError:
            break
        for listener in list(obj.listeners[event]):
            listener(obj, *args, **kwargs)
    
    roomData.removeComponent(obj, Messages)
