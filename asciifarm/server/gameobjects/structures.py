


from ..entity import Entity

from ..datacomponents import Attackable, Faction, Loot, LootMessage, Interact, Remove, Serialise, Static, Create, Solid, Occupied
from ..template import Template

entities = {}

entities["wall"] = lambda: Entity(sprite="wall", height=2, dataComponents=[Static("wall"), Solid])


entities["rock"] = lambda: Entity(sprite="rock", height=10, dataComponents=[Static("rock"), Solid])

entities["tree"] = lambda: Entity(sprite="tree", height=3, dataComponents=[Static("tree"), Solid])

entities["house"] = lambda: Entity(sprite="house", height=3, dataComponents=[Static("house"), Solid])

entities["fence"] = lambda: Entity(sprite="fence", height=1, dataComponents=[Static("fence"), Solid])


entities["builtwall"] = lambda health=None: Entity(
    sprite="builtwall",
    height=2,
    dataComponents=[
        Faction.NONE,
        Attackable(health=health, maxHealth=100, onDie=[LootMessage]),
        Serialise(
            lambda obj, roomData:
                Template("builtwall", health=roomData.getComponent(obj, Attackable).health)
        ),
        Loot(["stone"]),
        Solid
    ]
)


entities["closeddoor"] = lambda: Entity(sprite="closeddoor", name="door", height=2, dataComponents=[Interact(Remove, Create(Template("opendoor"))), Static("closeddoor"), Solid])

entities["opendoor"] = lambda: Entity(sprite="opendoor", name="door", height=1, dataComponents=[Interact(Remove, Create(Template("closeddoor"))), Static("opendoor"), Occupied])


entities["engraved"] = lambda c: Entity(sprite="engravedwall-"+c, height=2, dataComponents=[Static("wall", c), Solid])
