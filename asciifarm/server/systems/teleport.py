
from ..system import system
from ..datacomponents import Portal, EnterMessage

@system([EnterMessage, Portal])
def teleport(obj, roomData, messages, portal):
    for message in messages:
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

