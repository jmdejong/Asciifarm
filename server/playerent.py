
from placable import GameObject
import event

class Player(GameObject):
    
    char = 'player'
    size = 2
    direction = None
    attributes = {}
    slowness = 2
    
    def __init__(self, room, name=None):
        self.controller = {}
        self.room = room
        self.name = name or str(id(self))
        self.ground = None
        self.holding = None
        self.moveCooldown = 0
        room.addUpdateListener(self.update, self)
        self.event = event.Event()
    
    def setController(self, controller):
        self.controller = controller
    
    def place(self, ground):
        if self.ground:
            self.ground.removeObj(self)
        ground.addObj(self)
        self.ground = ground
            
    
    def update(self):
        self.moveCooldown = max(self.moveCooldown-1, 0)
        
        if "action" in self.controller:
            action = self.controller["action"]
            
            if action in self.ground.getNeighbours() and self.moveCooldown <= 0:
                newPlace = self.ground.getNeighbours()[action]
                
                if newPlace.accessible():
                    self.place(newPlace)
                    self.moveCooldown = self.slowness
                    newPlace.onEnter(self)
                    
    
    def inventoryAdd(self, obj):
        if not self.holding:
            self.holding = obj
        else:
            self.ground.addObj(obj)
    
    def inventoryRemove(self, obj):
        if obj == self.holding:
            self.holding = None
            return True
        return False
    
    def getActions(self):
        actions = set()
        if self.holding:
            actions.add("drop")
        else:
            actions.add("take")
        return actions
    
    def performAction(self, action, other):
        ofn = other.getInteractions().get(action)
        if not ofn:
            return
        ofn(self)
        
    
    def getNearObjects(self):
        places = {self.ground} | set(self.ground.getNeighbours().values())
        objects = set()
        for place in places:
            objects |= {obj for obj in place.getObjs()}
        objects.discard(self)
        return objects
    
    def getNearItems(self):
        items = self.getNearObjects() | set(self.getInventory())
        return items
    
    def remove(self):
        self.ground.removeObj(self)
        self.room.removeUpdateListener(self)
    
    def getEvent(self):
        return self.event
    
    def getGround(self):
        return self.ground
    
    def getInventory(self):
        if self.holding:
            return [self.holding]
        else:
            return []
