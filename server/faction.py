
class Faction:
    
    def __init__(self):
        self.enemies = set()
    
    def hates(self, faction):
        self.enemies.add(faction)
        if not faction.isEnemy(self):
            faction.hates(self)
    
    def isEnemy(self, faction):
        return faction in self.enemies


NEUTRAL = Faction() # doesn't hate anyone

GOOD = Faction() # players and allies
EVIL = Faction() # monsters and other enemies

EVIL.hates(GOOD)

NONE = Faction() # things that can always be attacked

GOOD.hates(NONE)
EVIL.hates(NONE)
