
from .. import faction
from ..component import Component

class Alignment(Component):
    
    def __init__(self, faction):
        self.faction = faction
    
    def getFaction(self):
        return self.faction
    
    def isEnemy(self, obj):
        alignment = obj.getComponent("alignment")
        if not alignment:
            return False
        return self.faction.isEnemy(alignment.getFaction())
    
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.faction = faction.factions[self.faction.getName()]
    
    def toJSON(self):
        return self.faction.getName()
    
    @classmethod
    def fromJSON(cls, facName):
        return cls(faction.factions[facName])
