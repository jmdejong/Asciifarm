

from ..system import system

@system(["move"])
def move(obj, roomData):
    movable = obj.dataComponents["move"]
    
    neighbours = obj.getGround().getNeighbours()
    if movable.canMove(obj, movable.direction) and roomData.getStamp() > movable.moveReady:
        newPlace = neighbours[movable.direction]
        
        if newPlace.accessible():
            obj.place(newPlace)
            movable.moveReady = roomData.getStamp() + movable.slowness
            obj.trigger("move")
        
    movable.direction = None

