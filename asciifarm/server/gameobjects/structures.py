


from ..entity import Entity

from ..components import StaticSerializer as Static
from ..components import CustomSerializer as Custom
from ..components import Change
from ..datacomponents import Attackable, Faction, Loot, Interact, Remove

entities = {}

entities["wall"] = lambda: Entity(sprite="wall", height=2, flags={"solid"}, components={"serialize": Static("wall")})


entities["rock"] = lambda: Entity(sprite="rock", height=10, flags={"solid"}, components={"serialize": Static("rock")})

entities["tree"] = lambda: Entity(sprite="tree", height=3, flags={"solid"}, components={"serialize": Static("tree")})

entities["house"] = lambda: Entity(sprite="house", height=3, flags={"solid"}, components={"serialize": Static("house")})

entities["fence"] = lambda: Entity(sprite="fence", height=1, flags={"solid"}, components={"serialize": Static("fence")})


entities["builtwall"] = lambda health=None: Entity(
    sprite="builtwall", height=2, flags={"solid"}, components={
        "serialize": Custom(
            lambda obj: {
                "type": "builtwall",
                "kwargs": {"health": obj.getDataComponent(Attackable).health}
            }
        )
    }, dataComponents=[
        Faction.NONE,
        Attackable(health=health or maxHealth, maxHealth=100, onDie=[Loot([("stone", 1)])])
    ]
)


entities["closeddoor"] = lambda: Entity(sprite="closeddoor", name="door", height=2, flags={"solid"}, components={"serialize": Static("closeddoor")}, dataComponents=[Interact(Remove, Loot([("opendoor",)]))])

entities["opendoor"] = lambda: Entity(sprite="opendoor", name="door", height=1, flags={"occupied"}, components={"serialize": Static("opendoor")}, dataComponents=[Interact(Remove, Loot([("closeddoor",)]))])


entities["engraved"] = lambda c: Entity(sprite="engravedwall-"+c, height=2, flags={"solid"}, components={"serialize": Static("wall", c)})
