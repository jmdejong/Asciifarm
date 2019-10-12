
from ..system import system
from ..datacomponents import UseMessage, Buildable, Remove, Inventory
from .. import gameobjects

@system([UseMessage, Buildable])
def build(obj, roomData, use, buildable):
    actor = use[0].actor
    ground = actor.getGround()
    for needed in buildable.flagsneeded:
        if not ground.hasFlag(needed):
            return
    for blocking in buildable.blockingflags:
        if ground.hasFlag(blocking):
            return
    builtobj = gameobjects.buildEntity(buildable.template, roomData, preserve=True)
    builtobj.place(ground)
    roomData.addComponent(obj, Remove)
    inv = roomData.getComponent(actor, Inventory)
    if inv is not None:
        inv.items.remove(obj)
        actor.trigger("inventorychange")
