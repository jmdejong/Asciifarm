
from ..system import system
from .. import gameobjects

from ..datacomponents import Create

@system([Create])
def create(obj, roomData, createmessages):
    for create in createmessages:
        for template in create.templates:
            created = gameobjects.buildEntity(template, roomData, preserve=True)
            created.place(obj.getGround())
