


class Inventory:
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        
    def attach(self, obj):
        pass
    
    def canAdd(self, item):
        return len(self.items) < self.capacity
    
    def add(self, item):
        self.items.append(item)
    
    def remove(self, item):
        self.items.remove(item) # should I catch here?
    
    def getItems(self):
        return list(self.items)


class InputController:
    
    def attach(self, obj):
        self.owner = obj
        if not obj.getComponent("inventory"):
            # todo: better exception
            raise Exception("InputController needs object with inventory")
    
    def control(self, action):
        if not action or len(action) < 1:
            return
        kind = action[0]
        if kind == "move" and len(action) > 1:
            self.owner.move(action[1])
        
        inventory = self.owner.getComponent("inventory")
        
        if kind == "take":
            for obj in self.owner.getNearObjects():
                if "takable" in obj.attributes and inventory.canAdd(obj): # temporary hack
                    inventory.add(obj)
                    obj.remove()
                    break
        
        if kind == "drop":
            for obj in inventory.getItems()[::-1]: # reverse inventory so it works as a stack
                inventory.remove(obj)
                obj.place(self.owner.getGround())
                break
    
    def getInteractions(self):
        return []

