

from ..system import system
from ..datacomponents import Move, EnterMessage

@system([Move])
def move(obj, roomData, movable):
    
    neighbours = obj.getGround().getNeighbours()
    if movable.canMove(obj, movable.direction) and roomData.getStamp() > movable.moveReady:
        newPlace = neighbours[movable.direction]
        
        if newPlace.accessible():
            for resident in newPlace.getObjs():
                roomData.addComponent(resident, EnterMessage(obj))
            obj.place(newPlace)
            movable.moveReady = roomData.getStamp() + movable.slowness
        
    movable.direction = None

