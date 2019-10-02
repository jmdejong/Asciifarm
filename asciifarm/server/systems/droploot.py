
from ..system import system
from .. import gameobjects

from ..datacomponents import Loot
from ..template import Template

@system([Loot])
def droploot(obj, roomData, loot):
    for template in loot.pick():
        dropped = gameobjects.buildEntity(template, roomData, preserve=True)
        dropped.place(obj.getGround())
