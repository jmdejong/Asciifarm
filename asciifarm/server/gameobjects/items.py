

from ..entity import Entity
from ..datacomponents import Static, Item
from ..components import Build, Equippable

entities = {}



entities["stone"] = lambda: Entity(sprite="stone", height=0.4, components={"item": Build("builtwall", flagsNeeded={"freeland"}, blockingFlags={"solid", "occupied"})}, dataComponents=[Static("stone"), Item])

entities["pebble"] = lambda: Entity(sprite="pebble", height=0.2, dataComponents=[Static("pebble"), Item])




entities["sword"] = lambda: Entity(sprite="sword", height=0.5, components={"item": Equippable("hand", {"strength": 5})}, dataComponents=[Static("sword"), Item])

entities["club"] = lambda: Entity(sprite="club", height=0.5, components={"item": Equippable("hand", {"strength": 3})}, dataComponents=[Static("club"), Item])

entities["weapon"] = lambda strength=0, name="weapon": Entity(sprite="sword", name=name, height=0.5, components={"item": Equippable("hand", {"strength": strength})}, dataComponents=[Static("weapon", strength=strength), Item])

entities["armour"] = lambda: Entity(sprite="armour", height=0.5, components={"item": Equippable("body", {"defence": 100})}, dataComponents=[Static("armour"), Item])



entities["hardwood"] = lambda: Entity(sprite="hardwood", height=0.4, components={"item": Build("builtwall", flagsNeeded={"freeland"}, blockingFlags={"solid", "occupied"})}, dataComponents=[Static("hardwood"), Item])
