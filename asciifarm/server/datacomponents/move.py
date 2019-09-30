
class Move:
    
    def __init__(self, slowness=1):
        self.direction = None
        self.slowness = slowness
        self.moveReady = 0
    
    def canMove(self, obj, direction):
        neighbours = obj.getGround().getNeighbours()
        return direction in neighbours and neighbours[direction].accessible()
