
from placable import GameObject
import event
import components

class Player(GameObject):
    
    char = 'player'
    size = 2
    attributes = {}
    slowness = 2
    
    def __init__(self, room, name=None):
        self.room = room
        self.name = name or str(id(self))
        self.holding = None
        self.moveCooldown = 0
        room.addUpdateListener(self.update, self)
        self.event = event.Event()
        
        self.moveDirection = None
        
        self.components = {
            "inventory": components.Inventory(10),
            "controller": components.InputController()
            }
        for component in self.components.values():
            component.attach(self)
    
    
    def move(self, direction):
        self.moveDirection = direction
    
    def update(self):
        self.moveCooldown = max(self.moveCooldown-1, 0)
            
        if self.moveDirection in self.ground.getNeighbours() and self.moveCooldown <= 0:
            newPlace = self.ground.getNeighbours()[self.moveDirection]
            
            if newPlace.accessible():
                self.place(newPlace)
                self.moveCooldown = self.slowness
                newPlace.onEnter(self)
            
            self.moveDirection = None
        
    
    def getNearObjects(self):
        objects = set(self.ground.getObjs())
        objects.discard(self)
        return objects
    
    def remove(self):
        super().remove()
        self.room.removeUpdateListener(self)
    
    def getEvent(self):
        return self.event
    
    def getComponent(self, name):
        return self.components.get(name, None)
    

