


from ..entity import Entity

from ..datacomponents import Attackable, Faction, Loot, LootMessage, Interact, Remove, Serialise, Static, Create
from ..template import Template

entities = {}

entities["wall"] = lambda: Entity(sprite="wall", height=2, flags={"solid"}, dataComponents=[Static("wall")])


entities["rock"] = lambda: Entity(sprite="rock", height=10, flags={"solid"}, dataComponents=[Static("rock")])

entities["tree"] = lambda: Entity(sprite="tree", height=3, flags={"solid"}, dataComponents=[Static("tree")])

entities["house"] = lambda: Entity(sprite="house", height=3, flags={"solid"}, dataComponents=[Static("house")])

entities["fence"] = lambda: Entity(sprite="fence", height=1, flags={"solid"}, dataComponents=[Static("fence")])


entities["builtwall"] = lambda health=None: Entity(
    sprite="builtwall",
    height=2,
    flags={"solid"},
    dataComponents=[
        Faction.NONE,
        Attackable(health=health, maxHealth=100, onDie=[LootMessage]),
        Serialise(
            lambda obj, roomData:
                Template("builtwall", health=roomData.getComponent(obj, Attackable).health)
        ),
        Loot(["stone"])
    ]
)


entities["closeddoor"] = lambda: Entity(sprite="closeddoor", name="door", height=2, flags={"solid"}, dataComponents=[Interact(Remove, Create(Template("opendoor"))), Static("closeddoor")])

entities["opendoor"] = lambda: Entity(sprite="opendoor", name="door", height=1, flags={"occupied"}, dataComponents=[Interact(Remove, Create(Template("closeddoor"))), Static("opendoor")])


entities["engraved"] = lambda c: Entity(sprite="engravedwall-"+c, height=2, flags={"solid"}, dataComponents=[Static("wall", c)])
