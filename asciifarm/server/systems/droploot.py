
from ..system import system
from .. import gameobjects

from ..datacomponents import Loot, LootMessage
from ..template import Template

@system([LootMessage, Loot])
def droploot(obj, roomData, _message, loot):
    for template in loot.pick():
        dropped = gameobjects.buildEntity(template, roomData, preserve=True)
        dropped.place(obj.getGround())
