
from ..system import system
from .. import gameobjects

from ..datacomponents import Loot
from ..template import Template

@system([Loot])
def droploot(obj, roomData, loot):
    for item, args, kwargs in loot.pick():
        template = Template(item, *args, **kwargs)
        dropped = gameobjects.buildEntity(template, roomData, preserve=True)
        dropped.place(obj.getGround())
