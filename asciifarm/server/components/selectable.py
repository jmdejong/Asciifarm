

from .component import Component


class Selectable(Component):
    
    def attach(self, obj):
        self.owner = obj
    
    def interact(self, obj):
        selector = obj.getComponent("select")
        if selector:
            selector.select(self.owner)



