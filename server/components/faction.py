
class Faction:
    
    def __init__(self):
        self.enemies = set()
    
    def hates(self, faction):
        self.enemies.add(faction)
        if not faction.isEnemyFaction(self):
            faction.hates(self)
    
    def isEnemyFaction(self, faction):
        return faction in self.enemies
    
    def isEnemy(self, obj):
        faction = obj.getComponent("alignment")
        if not faction:
            return False
        return self.isEnemyFaction(faction)


NEUTRAL = Faction() # doesn't hate anyone

GOOD = Faction() # players and allies
EVIL = Faction() # monsters and other enemies

GOOD.hates(EVIL)
