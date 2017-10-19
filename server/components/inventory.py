

class Inventory:
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
    
    def canAdd(self, item):
        return len(self.items) < self.capacity
    
    def add(self, item):
        self.items.insert(0, item)
    
    def drop(self, item):
        self.items.remove(item) # should I catch here?
    
    def getItems(self):
        return list(self.items)
