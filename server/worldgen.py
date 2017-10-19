
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
    g.set(4, 7, ["grass", "stone"])
    g.set(6, 8, ["grass", "pebble"])
    g.set(50, 25, ["grass", "rabbit", "rabbit", "rabbit", "rabbit"])
    g.set(11, 12, ["grass", "dummy"])
    g.set(19, 3, ["spiketrap"])
    g.set(30, 20, {"type": "roomexit", "args": ["basement", "stairup"], "kwargs": {"char": "stairdown"}})
    
    
    d = g.toDict()
    d["spawn"] = (10, 5)
    d["places"] = {
        "stairdown": (30, 20)
        }
    return d


def generateBasement():
    
    g = grid.Grid(64, 32, None)
    
    for x in range(20, 41):
        for y in range(15, 26):
            g.set(x, y, "wall")
    for x in range(21, 40):
        for y in range(16, 25):
            g.set(x, y, "ground")
    
    g.set(30, 20, {"type": "roomexit", "args": ["begin", "stairdown"], "kwargs": {"char": "stairup"}})
    d = g.toDict()
    d["spawn"] = (30, 20)
    d["places"] = {
        "stairup": (30, 20)
        }
    return d


def generateWorld():
    worlddata = {
        "begin": "begin",
        "rooms":{
            "begin": generateBeginRoom(),
            "basement": generateBasement()
            }
        }
    
    #import json
    #with open("worlddata.json", "w") as f:
        #json.dump(worlddata, f, indent=2)
    return worlddata
