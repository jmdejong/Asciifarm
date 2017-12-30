
from .component import Component


class Equippable(Component):
    """ item type for item that can be placed on the map to become something more static (like buildable walls or crops)"""
    
    def __init__(self, slot, stats={}):
        self.slot = slot
        self.stats = stats
    
    def attach(self, obj):
        self.owner = obj
    
    def getSlot(self):
        return self.slot
    
    def use(self, user):
        equipment = user.getComponent("equipment")
        if equipment.canEquip(self):
            equipment.equip(self.slot, self.owner)
        self.owner.trigger("drop")
    
    def getStat(self, stat):
        return self.stats.get(stat, 0)
    
    def toJSON(self):
        return {
            "slot": self.slot,
            "stats": self.stats
        }
    

