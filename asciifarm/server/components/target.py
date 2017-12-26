
from ..component import Component

class Target(Component):
    
    
    def attach(self, obj, roomData):
        self.owner = obj
        self.roomData = roomData
        roomData.addTarget(obj)
    
    def remove(self):
        self.roomData.removeTarget(self.owner)
