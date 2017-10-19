


class Inventory:
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
    
    def canAdd(self, item):
        return len(self.items) < self.capacity
    
    def add(self, item):
        self.items.append(item)
    
    def drop(self, item):
        self.items.remove(item) # should I catch here?
    
    def getItems(self):
        return list(self.items)


class InputController:
    
    def attach(self, obj, events):
        self.owner = obj
        
        for dep in {"inventory", "move"}:
            if not obj.getComponent(dep):
                # todo: better exception
                raise Exception("InputController needs object with " + dep + "component")
    
    def control(self, action):
        if not action or len(action) < 1:
            return
        kind = action[0]
        if kind == "move" and len(action) > 1:
            self.owner.getComponent("move").move(action[1])
        
        inventory = self.owner.getComponent("inventory")
        
        if kind == "take":
            for obj in self.owner.getNearObjects():
                if obj.isTakable() and inventory.canAdd(obj):
                    inventory.add(obj)
                    obj.remove()
                    break
        
        if kind == "drop":
            for obj in inventory.getItems()[::-1]: # reverse inventory so it works as a stack
                inventory.drop(obj)
                obj.place(self.owner.getGround())
                break
    
    def getInteractions(self):
        return []

class Move:
    
    def __init__(self, slowness=1):
        self.direction = None
        self.moveCooldown = 0
        self.slowness = slowness
    
    def attach(self, obj, events):
        self.owner = obj
        self.updateEvent = events["update"]
        self.updateEvent.addListener(self.update)
        
    
    def move(self, direction):
        self.direction = direction
    
    def update(self):
        
        self.moveCooldown = max(self.moveCooldown-1, 0)
        
        
        neighbours = self.owner.getGround().getNeighbours()
        if self.direction in neighbours and self.moveCooldown <= 0:
            newPlace = neighbours[self.direction]
            
            if newPlace.accessible():
                self.owner.place(newPlace)
                self.moveCooldown = self.slowness
                newPlace.onEnter(self.owner)
            
            self.direction = None
    
    def remove(self):
        self.updateEvent.removeListener(self.update)



class Item:
    
    def __init__(self, *args, **kwargs):
        pass



class Portal:
    
    def __init__(self, destRoom, destPos=None):
        self.destRoom = destRoom
        self.destPos = destPos
    
    def onEnter(self, obj):
        observable = obj.getComponent("observable")
        if observable:
            observable.trigger("changeroom", self.destRoom, self.destPos)

