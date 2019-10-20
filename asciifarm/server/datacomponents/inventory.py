

class Inventory:
    
    def __init__(self, capacity, items=None):
        self.items = items or []
        self.capacity = capacity
        self.changed = True
    
    def add(self, item):
        self.items.insert(0, item)
