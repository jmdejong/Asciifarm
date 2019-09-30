
class Faction:
    
    component = "faction"
    
    def __init__(self, name):
        self.name = name
        self.enemies = set()
    
    def hates(self, faction):
        self.enemies.add(faction)
        if not faction.isEnemy(self):
            faction.hates(self)
    
    def isEnemy(self, faction):
        return faction in self.enemies
    
    def getName(self):
        return self.name



NEUTRAL = Faction("neutral") # doesn't hate anyone

GOOD = Faction("good") # players and allies
EVIL = Faction("evil") # monsters and other enemies

EVIL.hates(GOOD)

NONE = Faction("none") # things that can always be attacked

GOOD.hates(NONE)
EVIL.hates(NONE)
NONE.hates(NONE)


factions = {}

for faction in [GOOD, EVIL, NEUTRAL, NONE]:
    factions[faction.getName()] = faction
