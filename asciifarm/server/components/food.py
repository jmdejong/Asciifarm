
from .component import Component


class Food(Component):
    
    
    def __init__(self, health):
        self.healing = health
    
    def attach(self, obj):
        self.owner = obj
    
    
    def use(self, user):
        fighter = user.getComponent("fighter")
        if fighter:
            fighter.heal(self.healing, self.owner)
            self.owner.trigger("drop")
    
    def toJSON(self):
        return {"health": self.healing}
