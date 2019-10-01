
from ..system import system
from .. import gameobjects

from ..datacomponents import Loot

@system([Loot])
def droploot(obj, roomData, loot):
    for item, args, kwargs in loot.pick():
        dropped = gameobjects.makeEntity(item, roomData, *args, preserve=True, **kwargs)
        dropped.place(obj.getGround())
