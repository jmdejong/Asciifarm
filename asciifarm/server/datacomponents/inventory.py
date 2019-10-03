

class Inventory:
    
    def __init__(self, capacity, items=None):
        self.items = items or []
        self.capacity = capacity
