
from .equippable import Equippable

class Equipment:
    
    def __init__(self, slots):
        self.slots = slots
        self.changed = True
    
    def getBonus(self, roomData, stat):
        bonus = 0
        for item in self.slots.values():
            if item is not None:
                bonus += roomData.getComponent(item, Equippable).stats.get(stat, 0)
        return bonus
