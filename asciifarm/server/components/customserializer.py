

from .component import Component

class CustomSerializer(Component):
    
    def __init__(self, fn):
        self.fn = fn
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, obj, roomData, stamp):
        self.roomData = roomData
    
    def serialize(self):
        return self.fn(self.owner, self.roomData)
