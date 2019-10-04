
from .component import Component
from ..datacomponents import Equipment

class Equippable(Component):
    """ item type for item that can be equipped"""
    
    def __init__(self, slot, stats=None):
        if stats is None:
            stats = {}
        self.slot = slot
        self.stats = stats
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData, stamp):
        self.roomData = roomData
    
    def getSlot(self):
        return self.slot
    
    def use(self, user):
        equipment = self.roomData.getComponent(user, Equipment)
        if self.slot in equipment.slots and equipment.slots[self.slot] is None:
            # Later it should be able to replace whatever is in the slot, but I don't want to deal with that now
            # therefore, it can currently only be placed in empty slots
            equipment[self.slot] = self.owner
            #self.equipped = True
        #equipment = user.getComponent("equipment")
        #if equipment.canEquip(self):
            #equipment.equip(self.slot, self.owner)
        self.owner.trigger("drop")
    
    def getStat(self, stat):
        return self.stats.get(stat, 0)
    
    def toJSON(self):
        return {
            "slot": self.slot,
            "stats": self.stats
        }
    

