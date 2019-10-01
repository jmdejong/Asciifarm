
from ..system import system
from ..datacomponents import Inbox

@system([Inbox])
def clearinbox(obj, roomData, inbox):
    roomData.removeComponent(obj, Inbox)
