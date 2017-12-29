
from .component import Component
from ..entity import Entity

class Inventory(Component):
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        self.owner = None
    
    def attach(self, obj, roomData):
        self.owner = obj
        obj.addListener("take", self.onTake)
    
    def canAdd(self, item):
        return len(self.items) < self.capacity
    
    def add(self, item):
        self.items.insert(0, item)
        item.addListener("drop", self.onDrop)
        self.owner.trigger("inventorychange")
    
    def drop(self, item):
        if item in self.items:
            self.items.remove(item)
            self.owner.trigger("inventorychange")
    
    def getItems(self):
        return list(self.items)
    
    def onDrop(self, item, action, *data):
        self.drop(item)
    
    def onTake(self, o, item=None, *data):
        self.add(item)
    
    def remove(self):
        self.owner = None
    
    
    def toJSON(self):
        return {
            "capacity": self.capacity,
            "items": [item.toJSON() for item in self.items]
        }
    
    @classmethod
    def fromJSON(cls, data):
        obj = cls(data["capacity"])
        obj.items = [Entity.fromJSON(item) for item in data["items"]]
        return obj
