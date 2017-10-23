

class Alignment:
    
    def __init__(self, faction):
        self.faction = faction
    
    def getFaction(self):
        return self.faction
    
    def isEnemy(self, obj):
        alignment = obj.getComponent("alignment")
        if not alignment:
            return False
        return self.faction.isEnemy(alignment.getFaction())
