
from .component import Component


class Portal(Component):
    
    def __init__(self, destRoom, destPos=None, mask=(False, False)):
        self.destRoom = destRoom
        self.origin = destPos
        self.mask = mask
    
    def attach(self, obj):
        obj.addListener("objectenter", self.onEnter)
        self.owner = obj
        
    
    def onEnter(self, owner, obj, *data):
        offset = self.owner.getGround().getPos()
        if self.origin is None:
            dest = None
        elif isinstance(self.origin, str):
            dest = self.origin
        else:
            dest = tuple(
                self.origin[i] + (offset[i] if self.mask[i] else 0)
                for i in range(2)
            )
        obj.trigger("changeroom", self.destRoom, dest)
    
    def toJSON(self):
        return {
            "destRoom": self.destRoom,
            "destPos": self.origin,
            "mask": self.mask
        }

