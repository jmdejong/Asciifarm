
from .component import Component

class Target(Component):
    
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, obj, roomData):
        self.roomData = roomData
        roomData.addTarget(obj)
    
    def remove(self):
        self.roomData.removeTarget(self.owner)
