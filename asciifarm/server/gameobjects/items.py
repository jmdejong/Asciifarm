

from ..entity import Entity
from ..components import StaticSerializer as Static
from ..components import Build, Item, Equippable

entities = {}



entities["stone"] = lambda: Entity(sprite="stone", height=0.4, components={"item": Build("builtwall", flagsNeeded={"freeland"}, blockingFlags={"solid", "occupied"}), "serialize": Static("stone")})

entities["pebble"] = lambda: Entity(sprite="pebble", height=0.2, components={"item": Item(), "serialize": Static("pebble")})




entities["sword"] = lambda: Entity(sprite="sword", height=0.5, components={"item": Equippable("hand", {"strength": 5}), "serialize": Static("sword")})

entities["club"] = lambda: Entity(sprite="club", height=0.5, components={"item": Equippable("hand", {"strength": 3}), "serialize": Static("club")})

entities["eldritch_sword"] = lambda: Entity(sprite="sword", name="eldritch sword", height=0.5, components={"item": Equippable("hand", {"strength": 500}), "serialize": Static("eldritch_sword")})

entities["armour"] = lambda: Entity(sprite="armour", height=0.5, components={"item": Equippable("body", {"defense": 100}), "serialize": Static("armour")})



entities["hardwood"] = lambda: Entity(sprite="hardwood", height=0.4, components={"item": Build("builtwall", flagsNeeded={"freeland"}, blockingFlags={"solid", "occupied"}), "serialize": Static("hardwood")})
