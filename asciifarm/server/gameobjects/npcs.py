

from ..entity import Entity

from ..components import StaticSerializer as Static
from ..components import Alignment, Fighter, Loot, MonsterAi, Move, RandomWalkController, Trap

from .. import faction

entities = {}


entities["rabbit"] = lambda: Entity(
    sprite="rabbit", name="bunny", height=1, components={"move": Move(slowness=4), "controller": RandomWalkController(moveChance=0.05), "serialize": Static("rabbit")})


entities["goblin"] = lambda home=None: Entity(sprite="goblin", height=1.2, components={
        "move": Move(slowness=3),
        "fighter": Fighter(maxHealth=15, strength=5, slowness=8),
        "alignment": Alignment(faction.EVIL),
        "controller": MonsterAi(viewDist=8, moveChance=0.02, home=home),
        "loot": Loot([("sword", .05), ("club", .1), ("radishes", .25)])
        })

entities["troll"] = lambda home=None: Entity(sprite="troll", height=1.8, components={
        "move": Move(slowness=4),
        "fighter": Fighter(maxHealth=75, strength=15, slowness=10),
        "alignment": Alignment(faction.EVIL),
        "controller": MonsterAi(viewDist=8, moveChance=0.01, home=home),
        "loot": Loot([("stone", 1), ("stone", .3), ("pebble", .5), ("pebble", .5), ("pebble", .5)])
        })

entities["rat"] = lambda home=None: Entity(sprite="rat", height=1, components={
        "move": Move(slowness=3),
        "fighter": Fighter(maxHealth=8, strength=2, slowness=6),
        "alignment": Alignment(faction.EVIL),
        "controller": MonsterAi(viewDist=3, moveChance=0.08, home=home, homesickness=0.1),
        "loot": Loot([("radishseed", 0.9), ("radishseed", 0.3)])
        })




entities["dummy"] = lambda: Entity(
    sprite="dummy", height=1, flags={"occupied"}, components={"fighter": Fighter(maxHealth=20, strength=0), "alignment": Alignment(faction.NONE)})

entities["spiketrap"] = lambda damage=25: Entity(
    sprite="spikes", height=1, flags={"occupied"}, components={"fighter": Fighter(maxHealth=25, strength=damage, attackable=False), "collision": Trap(), "serialize": Static("spiketrap")})
