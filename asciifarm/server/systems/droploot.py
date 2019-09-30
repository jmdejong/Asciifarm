
from ..system import System
from .. import gameobjects

from ..datacomponents import Loot

@System([Loot])
def droploot(obj, roomData, loot):
    for item, args, kwargs in loot.pick():
        dropped = gameobjects.makeEntity(item, roomData, *args, preserve=True, **kwargs)
        dropped.place(obj.getGround())
