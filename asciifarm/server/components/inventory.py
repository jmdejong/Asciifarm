
from .component import Component
from .. import gameobjects

class Inventory(Component):
    
    def __init__(self, capacity, initialItems=None):
        if initialItems is None:
            initialItems = []
        self.capacity = capacity
        self.items = []
        self.owner = None
        for item in initialItems[::-1]:
            if item:
                self.add(item)
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("take", self.onTake)
    
    def canAdd(self, item):
        return len(self.items) < self.capacity
    
    def canAddAll(self, items):
        return len(self.items) + len(items) <= self.capacity
    
    def add(self, item):
        self.items.insert(0, item)
        item.addListener("drop", self.onDrop)
        if self.owner:
            self.owner.trigger("inventorychange")
    
    def drop(self, item):
        if self.has(item):
            self.items.remove(item)
            if self.owner:
                self.owner.trigger("inventorychange")
    
    def getItems(self):
        return list(self.items)
    
    def has(self, item):
        return item in self.items
    
    def onDrop(self, item, *data):
        self.drop(item)
    
    def onTake(self, o, item=None, *data):
        self.add(item)
    
    def remove(self):
        self.owner = None
    
    
    def toJSON(self):
        return {
            "capacity": self.capacity,
            "items": [item.serialize() for item in self.items]
        }
    
    @classmethod
    def fromJSON(cls, data):
        obj = cls(data["capacity"], [gameobjects.createEntity(item) for item in data["items"]])
        return obj
