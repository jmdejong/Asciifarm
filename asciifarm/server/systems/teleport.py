
from ..system import System
from ..datacomponents import Inbox, Portal
from ..messages import EnterMessage

@System([Inbox, Portal])
def teleport(obj, roomData, inbox, portal):
    for message in inbox.messages:
        if isinstance(message, EnterMessage):
            offset = obj.getGround().getPos()
            if portal.origin is None:
                dest = None
            elif isinstance(portal.origin, str):
                dest = portal.origin
            else:
                dest = tuple(
                    portal.origin[i] + (offset[i] if portal.mask[i] else 0)
                    for i in range(2)
                )
            message.actor.trigger("changeroom", portal.destRoom, dest)

