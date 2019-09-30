

from ..entity import Entity

from ..components import StaticSerializer as Static
from ..components import Trap
from ..datacomponents import Fighter, Move, Attackable, AI, Faction, Loot

entities = {}


entities["rabbit"] = lambda: Entity(
    sprite="rabbit", name="bunny", height=1, components={"serialize": Static("rabbit")}, dataComponents=[AI(moveChance=0.05), Move(slowness=4)])


entities["goblin"] = lambda home=None: Entity(sprite="goblin", height=1.2, dataComponents=[
        Faction.EVIL,
        AI(viewDist=8, moveChance=0.02, home=home),
        Move(slowness=3),
        Attackable(maxHealth=15, onDie=[Loot([("sword", .05), ("club", .1), ("radishes", .25)])]),
        Fighter(strength=5, slowness=8)
        
    ]
)

entities["troll"] = lambda home=None: Entity(sprite="troll", height=1.8, dataComponents=[
        Faction.EVIL,
        AI(viewDist=8, moveChance=0.01, home=home),
        Move(slowness=4),
        Attackable(maxHealth=75, onDie=[Loot([("stone", 1), ("stone", .3), ("pebble", .5), ("pebble", .5), ("pebble", .5)])]),
        Fighter(strength=15, slowness=10)
        
    ]
)

entities["rat"] = lambda home=None: Entity(sprite="rat", height=1, dataComponents=[
        Faction.EVIL,
        AI(viewDist=3, moveChance=0.08, home=home, homesickness=0.1),
        Move(slowness=3),
        Attackable(maxHealth=8, onDie=[Loot([("radishseed", 0.9), ("radishseed", 0.3)])]),
        Fighter(strength=2, slowness=6)
    ]
)




entities["dummy"] = lambda: Entity(
    sprite="dummy", height=1, flags={"occupied"}, dataComponents=[
        Attackable(maxHealth=20),
        Faction.NONE
    ])

entities["spiketrap"] = lambda damage=15: Entity(sprite="spikes", height=1, flags={"occupied"}, components={
        "collision": Trap(),
        "serialize": Static("spiketrap")
    }, dataComponents=[Fighter(strength=damage, slowness=20)]
)
