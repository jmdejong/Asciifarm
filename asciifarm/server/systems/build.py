
from ..system import system
from ..datacomponents import UseMessage, Buildable, Remove, Inventory
from .. import gameobjects

@system([UseMessage, Buildable])
def build(obj, roomData, use, buildable):
    actor = use[0].actor
    ground = actor.getGround()
    print("building")
    groundFlags = ground.getFlags()
    if not buildable.flagsneeded <= groundFlags or groundFlags & buildable.blockingflags: # <= means subset when applied on sets
        # groundFlags must contain all of self.flagsNeeded, and none of self.blockingFlags
        return
    builtobj = gameobjects.buildEntity(buildable.template, roomData, preserve=True)
    builtobj.place(ground)
    roomData.addComponent(obj, Remove)
    inv = roomData.getComponent(actor, Inventory)
    if inv is not None:
        inv.items.remove(obj)
        actor.trigger("inventorychange")
