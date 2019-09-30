
from .component import Component
from ..datacomponents import Fighter

class Trap(Component):
    
    
    def attach(self, obj):
        
        if not obj.getDataComponent(Fighter):
            # todo: better exception
            raise Exception("Trap needs object with fighter component")
        
        self.owner = obj
        self.fighter = obj.getComponent("fighter")
        
        obj.addListener("objectenter", self.onEnter)
        
    
    def onEnter(self, owner, obj=None, *data):
        self.owner.getDataComponent(Fighter).target = obj
    

