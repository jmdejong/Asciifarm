
from ..system import System
from .. import gameobjects

from ..datacomponents import Dead, Loot

@System([Dead, Loot])
def droploot(obj, roomData, _dead, loot):
    print("droploot", roomData.getStamp())
    for item, args, kwargs in loot.pick():
        dropped = gameobjects.makeEntity(item, roomData, *args, preserve=True, **kwargs)
        dropped.place(obj.getGround())
