
from ..component import Component
from ..entity import Entity


class Equipment(Component):
    
    
    def __init__(self, slots={}):
        self.slots = slots
    
    def attach(self, obj, roomData):
        self.owner = obj
    
    def getBonus(self, skill):
        return sum(item.getComponent("item").getStat(skill) for item in self.slots.values() if item)
    
    def equip(self, slot, item):
        if slot in self.slots:
            oldItem = self.slots[slot]
            if oldItem:
                self.owner.trigger("take", oldItem)
            self.slots[slot] = item
        else:
            # todo: better exception
            raise Exception("No such slot")
    
    def unEquip(self, slot):
        if slot in self.slots:
            self.slots[slot] = None
    
    def getSlots(self):
        return self.slots.copy()
    
    def canEquip(self, item):
        return item.getSlot() in self.slots
    
    
    def toJSON(self):
        return {
            slotName: item.toJSON()
            for slotName, item in self.slots.items()
        }
    
    @classmethod
    def fromJSON(cls, slots):
        return cls({
            slotName: Entity.fromJSON(item)
            for slotname, item in slots.items()
        })
    
    
