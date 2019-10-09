

from ..entity import Entity
from ..datacomponents import Static, Item, Equippable, Buildable
from ..template import Template

entities = {}



entities["stone"] = lambda: Entity(sprite="stone", height=0.4, dataComponents=[Static("stone"), Item, Build(Template("builtwall"), flagsneeded={"freeland"}, blockingflags={"solid", "occupied"})])

entities["pebble"] = lambda: Entity(sprite="pebble", height=0.2, dataComponents=[Static("pebble"), Item])




entities["sword"] = lambda: Entity(sprite="sword", height=0.5, dataComponents=[Static("sword"), Item, Equippable("hand", {"strength": 5})])

entities["club"] = lambda: Entity(sprite="club", height=0.5, dataComponents=[Static("club"), Item, Equippable("hand", {"strength": 3})])

entities["weapon"] = lambda strength=0, name="weapon": Entity(sprite="sword", name=name, height=0.5, dataComponents=[Static("weapon", strength=strength), Item. Equippable("hand", {"strength": strength})])

entities["armour"] = lambda: Entity(sprite="armour", height=0.5, dataComponents=[Static("armour"), Item, Equippable("body", {"defence": 100})])



#entities["hardwood"] = lambda: Entity(sprite="hardwood", height=0.4, components={"item": Build("builtwall", flagsNeeded={"freeland"}, blockingFlags={"solid", "occupied"})}, dataComponents=[Static("hardwood"), Item])
