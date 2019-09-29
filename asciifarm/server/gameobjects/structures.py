


from ..entity import Entity
from .. import faction

from ..components import StaticSerializer as Static
from ..components import CustomSerializer as Custom
from ..components import Change
from ..components import Loot
from ..datacomponents import Attackable

entities = {}

entities["wall"] = lambda: Entity(sprite="wall", height=2, flags={"solid"}, components={"serialize": Static("wall")})


entities["rock"] = lambda: Entity(sprite="rock", height=10, flags={"solid"}, components={"serialize": Static("rock")})

entities["tree"] = lambda: Entity(sprite="tree", height=3, flags={"solid"}, components={"serialize": Static("tree")})

entities["house"] = lambda: Entity(sprite="house", height=3, flags={"solid"}, components={"serialize": Static("house")})

entities["fence"] = lambda: Entity(sprite="fence", height=1, flags={"solid"}, components={"serialize": Static("fence")})


entities["builtwall"] = lambda health=None: Entity(
    sprite="builtwall", height=2, flags={"solid"}, components={
        "loot": Loot([("stone", 1)]),
        "serialize": Custom(
            lambda obj: {
                "type": "builtwall",
                "kwargs": {"health": obj.dataComponents["attackable"].health}
            }
        )
    }, dataComponents={
        "faction": faction.NONE,
        "attackable": Attackable(health=health or maxHealth, maxHealth=100)
    }
)


entities["closeddoor"] = lambda: Entity(sprite="closeddoor", name="door", height=2, flags={"solid"}, components={"interact": Change("opendoor"), "serialize": Static("closeddoor")})

entities["opendoor"] = lambda: Entity(sprite="opendoor", name="door", height=1, flags={"occupied"}, components={"interact": Change("closeddoor"), "serialize": Static("opendoor")})

#entities["builtcloseddoor"] = lambda health=None: Entity(sprite="closeddoor", name="door", height=2, flags={"solid"}, components={
    #"interact": Change(transferComponents={"fighter"}),
    #"fighter": Fighter(maxHealth=100, health=health, strength=0),
    #"alignment": Alignment(faction.NONE),
    #"loot": Loot([("hardwood", 1)])})

#entities["builtopendoor"] = lambda health=None: Entity(sprite="opendoor", name="door", height=1, flags={"occupied"}, components={
    #"interact": Change(),
    #"fighter": Fighter(maxHealth=100, health=health, strength=0),
    #"alignment": Alignment(faction.NONE),
    #"loot": Loot([("hardwood", 1)])})


entities["engraved"] = lambda c: Entity(sprite="engravedwall-"+c, height=2, flags={"solid"}, components={"serialize": Static("wall", c)})
