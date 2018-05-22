

from ..entity import Entity
from ..components import Build, Food, Growing, Harvest, Loot
from ..components import StaticSerializer as Static

entities = {}

entities["sownradishseed"] = lambda: Entity(sprite="seed", height=0.05, name="plantedseed", flags={"occupied"}, components={"grow": Growing("youngradish", 2000)})
entities["sownseed"] = entities["sownradishseed"]

entities["youngradishplant"] = lambda: Entity(sprite="youngplant", height=0.5, flags={"occupied"}, components={"grow": Growing("radishplant", 4000)})
entities["youngplant"] = entities["youngradishplant"]

entities["radishplant"] = lambda: Entity(sprite="plant", name="radishplant", height=1.2, flags={"occupied"}, components={
        "interact": Harvest(),
        "loot": Loot([("radishseed", .92), ("radishseed", .20), ("radishes", .8), ("radishes", .4)]),
        "serialize": Static("radishplant")
        })
entities["plant"] = entities["radishplant"]

entities["radishes"] = lambda: Entity(sprite="food", name="radishes", height=0.3, components={"item": Food(2), "serialize": Static("radishes")})
entities["food"] = entities["radishes"]

entities["radishseed"] = lambda: Entity(sprite="seed", name="radishseed", height=0.2, components={"item": Build("sownseed", flagsNeeded={"soil"}, blockingFlags={"occupied", "solid"}), "serialize": Static("radishseed")})
entities["seed"] = entities["radishseed"]
