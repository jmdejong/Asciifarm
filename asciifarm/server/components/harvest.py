
from .component import Component

class Harvest(Component):
    
    
    def attach(self, obj, roomData):
        self.owner = obj
    
    def interact(self, obj):
        self.owner.trigger("die") # loot component will register this
        self.owner.remove()
