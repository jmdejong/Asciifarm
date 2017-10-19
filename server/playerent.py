
from placable import GameObject
import event
import components

class Player(GameObject):
    
    char = 'player'
    size = 2
    attributes = {}
    
    def __init__(self, events, name=None, components={}):
        self.roomEvents = events
        self.name = name or str(id(self))
        self.event = event.Event()
        
        self.moveDirection = None
        
        self.components = components
        
        for component in self.components.values():
            if hasattr(component, "attach"):
                component.attach(self, self.roomEvents)
        
    
    def getNearObjects(self):
        objects = set(self.ground.getObjs())
        objects.discard(self)
        return objects
    
    def remove(self):
        super().remove()
        for component in self.components.items():
            if hasattr(component, "remove"):
                component.remove()
    
    def getEvent(self):
        return self.event
    
    def getComponent(self, name):
        return self.components.get(name, None)
    

