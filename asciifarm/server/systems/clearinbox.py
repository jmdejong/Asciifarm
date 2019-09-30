
from ..system import System
from ..datacomponents import Inbox

@System([Inbox])
def clearinbox(obj, roomData, inbox):
    roomData.removeComponent(obj, Inbox)
