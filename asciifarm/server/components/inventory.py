

class Inventory:
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        self.owner = None
    
    def attach(self, obj, roomData):
        self.owner = obj
    
    def canAdd(self, item):
        return len(self.items) < self.capacity
    
    def add(self, item):
        self.items.insert(0, item)
        item.addListener(self.onItemUpdate)
        self.owner.trigger("inventorychange")
    
    def drop(self, item):
        if item in self.items:
            self.items.remove(item)
            self.owner.trigger("inventorychange")
    
    def getItems(self):
        return list(self.items)
    
    def onItemUpdate(self, item, action, *data):
        if action == "drop":
            self.drop(item)
    
    def remove(self):
        self.owner = None
