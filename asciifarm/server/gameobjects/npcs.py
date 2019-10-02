

from ..entity import Entity

from ..datacomponents import Fighter, Move, Attackable, AI, Faction, Loot, LootMessage, Trap, Static

entities = {}


entities["rabbit"] = lambda: Entity(
    sprite="rabbit", name="bunny", height=1, dataComponents=[AI(moveChance=0.05), Move(slowness=4), Static("rabbit")]
)


entities["goblin"] = lambda home=None: Entity(sprite="goblin", height=1.2, dataComponents=[
        Faction.EVIL,
        AI(viewDist=8, moveChance=0.02, home=home),
        Move(slowness=3),
        Attackable(maxHealth=15, onDie=[LootMessage]),
        Fighter(strength=5, slowness=8),
        Loot([("sword", .05), ("club", .1), ("radishes", .25)])
    ]
)

entities["troll"] = lambda home=None: Entity(sprite="troll", height=1.8, dataComponents=[
        Faction.EVIL,
        AI(viewDist=8, moveChance=0.01, home=home),
        Move(slowness=4),
        Attackable(maxHealth=75, onDie=[LootMessage]),
        Fighter(strength=15, slowness=10),
        Loot([("stone", 1), ("stone", .3), ("pebble", .5), ("pebble", .5), ("pebble", .5)])
    ]
)

entities["rat"] = lambda home=None: Entity(sprite="rat", height=1, dataComponents=[
        Faction.EVIL,
        AI(viewDist=3, moveChance=0.08, home=home, homesickness=0.1),
        Move(slowness=3),
        Attackable(maxHealth=8, onDie=[LootMessage]),
        Fighter(strength=2, slowness=6),
        Loot([("radishseed", 0.9), ("radishseed", 0.3)])
    ]
)




entities["dummy"] = lambda: Entity(
    sprite="dummy", height=1, flags={"occupied"}, dataComponents=[
        Attackable(maxHealth=20),
        Faction.NONE
    ])

entities["spiketrap"] = lambda damage=15: Entity(
    sprite="spikes",
    height=1,
    flags={"occupied"},
    dataComponents=[Fighter(strength=damage, slowness=10), Trap(), Static("spiketrap")]
)
