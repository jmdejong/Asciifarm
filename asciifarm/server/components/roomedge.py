
from .component import Component

# todo: combine with portal

class RoomEdge(Component):
    
    def __init__(self, destRoom, destOrigin=(0,0), mask=(True, True)):
        self.destRoom = destRoom
        self.origin = destOrigin
        self.mask = mask
    
    def attach(self, obj, roomData):
        obj.addListener("objectenter", self.onEnter)
        self.owner = obj
        
    
    def onEnter(self, owner, obj=None, *data):
        offset = self.owner.getGround().getPos()
        dest = tuple(
            self.origin[i] + (offset[i] if self.mask[i] else 0)
            for i in range(2)
        )
        obj.trigger("changeroom", self.destRoom, dest)
    
    def toJSON(self):
        return {
            "destRoom": self.destRoom,
            "destPos": self.destPos
        }

