
from .component import Component
from ..datacomponents import Dead

class Harvest(Component):
    
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData, stamp):
        self.roomData = roomData
    
    def interact(self, obj):
        self.roomData.addComponent(self.owner, Dead)
        self.owner.remove()
