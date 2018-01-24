
from .component import Component


class HomePortal(Component):
    
    def __init__(self, roomName="*home:{}"):
        self.roomName = roomName
    
    def attach(self, obj):
        obj.addListener("objectenter", self.onEnter)
        self.owner = obj
        
    
    def onEnter(self, owner, obj=None, *data):
        
        obj.trigger("changeroom", self.destRoom, dest)
    
    def toJSON(self):
        return {
            "destRoom": self.destRoom,
            "destPos": self.origin,
            "mask": self.mask
        }

