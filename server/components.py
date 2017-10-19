


class Inventory:
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
    
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
    
    def control(self, action):
        if not action or len(action) < 1:
            return
        #print(action)
        kind = action[0]
        if kind == "move" and len(action) > 1:
            #self.controller["action"] = action[1]
            self.owner.move(action[1])
        
        if kind == "take":
            #print(action)
            for obj in self.owner.getNearObjects():
                if "takable" in obj.attributes: # temporary hack
                    self.owner.inventory.add(obj)
                    obj.remove()
                    break
        
        if kind == "drop":
            for obj in self.owner.getInventory()[::-1]: # reverse inventory so it works as a stack
                self.owner.inventory.remove(obj)
                obj.place(self.owner.getGround())
                break

