
import grid



# module for generating some test rooms. should probably be replaced

def generateBeginRoom():
    
    g = grid.Grid(64, 32, "grass")
    
    
    
    for x in range(20, 41):
        for y in range(15, 26):
            g.set(x, y, "ground")
    
    for x in range(20, 41):
        g.set(x, 15, "wall")
        g.set(x, 25, "wall")
    
    for y in range(16, 25):
        g.set(20, y, "wall")
        g.set(40, y, "wall")
    
    g.set(20, 19, "ground")
    g.set(20, 20, "ground")
    
    for x in range(25, 32):
        for y in range(6, 11):
            g.set(x, y, "water")
    for x in range(24, 34):
        for y in range(7, 10):
            g.set(x, y, "water")
    
    g.set(3, 8, ["grass", "stone"])
    
    return g.toDict()


def generateWorld():
    return {
        "begin": "begin",
        "rooms":{
            "begin": generateBeginRoom()
            }
        }
