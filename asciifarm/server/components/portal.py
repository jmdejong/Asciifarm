
from .component import Component


class Portal(Component):
    
    def __init__(self, destRoom, destPos=None):
        self.destRoom = destRoom
        self.destPos = destPos
        if isinstance(self.destPos, list):
            destPos = tuple(destPos)
    
    def attach(self, obj, roomData):
        obj.addListener("objectenter", self.onEnter)
    
    def onEnter(self, owner, obj=None, *data):
        obj.trigger("changeroom", self.destRoom, self.destPos)
    
    def toJSON(self):
        return {
            "destRoom": self.destRoom,
            "destPos": self.destPos
        }

