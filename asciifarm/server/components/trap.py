
from .component import Component

class Trap(Component):
    
    
    def attach(self, obj, roomData):
        
        if not obj.getComponent("fighter"):
            # todo: better exception
            raise Exception("Trap needs object with fighter component")
        
        self.owner = obj
        self.fighter = obj.getComponent("fighter")
        
        obj.addListener("objectenter", self.onEnter)
        
    
    def onEnter(self, owner, obj=None, *data):
        self.fighter.attack(obj)
    

