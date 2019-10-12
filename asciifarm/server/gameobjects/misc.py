


from ..entity import Entity
from ..datacomponents import Portal, Static, Periodic, Remove, StartTimer, Spawner, SpawnMessage, FreeLand
from ..template import Template


entities = {}



entities["freeland"] = lambda: Entity(name="buildable", dataComponents=[Static("freeland"), FreeLand])

entities["spawner"] = lambda template, number, delay, sprite=None, name=None, height=0, setHome=False, initialSpawn=True: Entity(
    sprite=sprite, height=height, name=name, dataComponents=[
        StartTimer,
        SpawnMessage if initialSpawn else None,
        Periodic([StartTimer, SpawnMessage], interval=delay, randomise=True),
        Spawner(Template.fromJSON(template), number, setHome=setHome),
        Static("spawner", template, number, delay, sprite, name, height, setHome, initialSpawn)
    ]
)


entities["letter"] = lambda c: Entity(sprite="emptyletter-"+c, dataComponents=[Static("letter", c)])


entities["roomexit"] = lambda destRoom, destPos=None, mask=(False, False), sprite=" ", size=0: Entity(
    sprite=sprite, height=size, dataComponents=[
        Portal(destRoom, destPos, mask),
        Static(destRoom, destPos, mask, sprite, size)
    ]
)


entities["wound"] = lambda duration=4, height=0.2: Entity(sprite="wound", name="", height=height, dataComponents=[StartTimer(), Periodic([Remove], duration), Static(None)])

#entities["raindrop"] = lambda: Entity(sprite="raindrop", name="", height=10, components={"weather": Weather(speed=2.5, spread=0.2)}, dataComponents=[Static(None)})

#entities["snowflake"] = lambda: Entity(sprite="snowflake", name="", height=10, components={"weather": Weather(speed=1, spread=0.5), "serialize": Static(None)})
