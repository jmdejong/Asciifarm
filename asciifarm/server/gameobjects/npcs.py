

from ..entity import Entity

from ..components import StaticSerializer as Static
from ..components import Alignment, FighterData, Loot, MonsterAi, Move, RandomWalkController, Trap, AttackableData

from .. import faction

entities = {}


entities["rabbit"] = lambda: Entity(
    sprite="rabbit", name="bunny", height=1, components={"move": Move(slowness=4), "controller": RandomWalkController(moveChance=0.05), "serialize": Static("rabbit")})


entities["goblin"] = lambda home=None: Entity(sprite="goblin", height=1.2, components={
        "move": Move(slowness=3),
        "alignment": Alignment(faction.EVIL),
        "controller": MonsterAi(viewDist=8, moveChance=0.02, home=home),
        "loot": Loot([("sword", .05), ("club", .1), ("radishes", .25)])
    }, dataComponents={
        "attackable": Attackable.Data(maxHealth=15),
        "fighter": FighterData(strength=5, slowness=8)
    }
)

entities["troll"] = lambda home=None: Entity(sprite="troll", height=1.8, components={
        "move": Move(slowness=4),
        "alignment": Alignment(faction.EVIL),
        "controller": MonsterAi(viewDist=8, moveChance=0.01, home=home),
        "loot": Loot([("stone", 1), ("stone", .3), ("pebble", .5), ("pebble", .5), ("pebble", .5)])
    }, dataComponents={
        "attackable": AttackableData(maxHealth=75),
        "fighter": FighterData(strength=15, slowness=10)
    }
)

entities["rat"] = lambda home=None: Entity(sprite="rat", height=1, components={
        "move": Move(slowness=3),
        "alignment": Alignment(faction.EVIL),
        "controller": MonsterAi(viewDist=3, moveChance=0.08, home=home, homesickness=0.1),
        "loot": Loot([("radishseed", 0.9), ("radishseed", 0.3)])
    }, dataComponents={
        "attackable": AttackableData(maxHealth=8),
        "fighter": FighterData(strength=2, slowness=6)
    }
)




entities["dummy"] = lambda: Entity(
    sprite="dummy", height=1, flags={"occupied"}, components={"alignment": Alignment(faction.NONE)}, dataComponents={"attackable": AttackableData(maxHealth=20)})

entities["spiketrap"] = lambda damage=15: Entity(sprite="spikes", height=1, flags={"occupied"}, components={
        "collision": Trap(),
        "serialize": Static("spiketrap")
    }, dataComponents={
        "fighter": FighterData(strength=damage, slowness=20)
    }
)
