
from .component import Component

class Select(Component):
    
    def __init__(self):
        self.selection = None
    
    def attach(self, obj):
        self.owner = obj
    
    def select(self, obj=None):
        self.selection = obj
        self.owner.trigger("selection", obj)
        obj.trigger("selectedby", self.owner)
    
    def getSelected(self):
        return self.selection
    
