
from .component import Component


class Volatile(Component):
    
    
    def __init__(self, duration):
        self.duration = duration
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData):
        self.roomData = roomData
        roomData.setAlarm(roomData.getStamp() + self.duration, self.end)
    
    def end(self):
        self.owner.remove()
    
    
    def toJSON(self):
        # better not to save volatile entities in the first place...
        return {
            "duration": self.duration
            }
    
