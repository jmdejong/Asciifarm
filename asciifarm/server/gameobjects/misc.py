


from ..entity import Entity
from ..components import Spawner
from ..datacomponents import Portal, Static, Periodic, Remove, StartTimer


entities = {}



entities["freeland"] = lambda: Entity(name="buildable", flags={"freeland"}, dataComponents=[Static("freeland")])

entities["spawner"] = lambda objType, number, delay, sprite=None, name=None, height=0, setHome=False, initialSpawn=True, objArgs=None, objKwargs=None: Entity(
    sprite=sprite, height=height, name=name, components={
        "spawn": Spawner(objType, number, delay, setHome, initialSpawn, objArgs, objKwargs)
    }, dataComponents=[
        Static("spawner", objType, number, delay, sprite, name, height, setHome, initialSpawn, objArgs, objKwargs)
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
