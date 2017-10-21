

class Alignment:
    
    def __init__(self, faction):
        self.faction = faction
    
    def attach(self, obj, roomData):
        self.owner = obj
        self.roomData = roomData
        roomData.addTarget(obj)
    
    def getFaction(self):
        return self.faction
    
    def isEnemy(self, obj):
        alignment = obj.getComponent("alignment")
        if not alignment:
            return False
        return self.faction.isEnemy(alignment.getFaction())
    
    def remove(self):
        self.roomData.removeTarget(self.owner)
