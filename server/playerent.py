
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
            
            
            if action == "drop" and self.holding:
                self.ground.addObj(self.holding)
                self.holding = None
            
            if action == "take" and not self.holding:
                for obj in self.ground.getObjs():
                    if "takable" in obj.attributes:
                        self.ground.removeObj(obj)
                        self.holding = obj
                        break
    
    def pickup(self, obj):
        if not self.holding:
            self.holding = obj
        else:
            self.ground.addObj(obj)
    
    def drop(self):
        obj = self.holding
        self.holding = None
        self.ground.addObj(obj)
    
    def getActions(self):
        actions = {}
        if self.holding:
            actions["drop"] = self.drop
        else:
            actions["take"] = self.pickup
        return actions
    
    def performAction(self, action, other):
        fn = self.getActions().get(action)
        ofn = other.getInteractions().get(action)
        if not fn or not ofn:
            return
        fn(other)
        ofn(self)
        
    
    def getNearObjects(self):
        places = {self.ground} | set(self.ground.getNeighbours().values())
        #print(places)
        objects = set()
        for place in places:
            objects |= {obj for obj in place.getObjs()}
        #print(objects)
        return objects
    
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
