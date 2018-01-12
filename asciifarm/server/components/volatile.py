from .. import timeout
from .component import Component


class Volatile(Component):
    
    
    def __init__(self, duration):
        self.duration = duration
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData):
        self.roomData = roomData
        self.timeout = timeout.Timeout(roomData.getEvent("update"), self.duration, self.end)
    
    def end(self, to):
        self.owner.remove()
    
    def remove(self):
        self.timeout.remove()
    
    
    def toJSON(self):
        # better not to save volatile entities in the first place...
        return {
            "duration": self.duration
            }
    
