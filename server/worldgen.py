
import grid


""" Temporary module for generating rooms

Eventually it's probably better to make a loader and load rooms from JSON
However, this module is still very convenient for testing
"""

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
    g.set(37, 18, ["spiketrap"])
    g.set(21, 16, ["grass", "seed"])
    g.set(21, 17, ["grass", "seed"])
    g.set(22, 16, ["grass", "seed"])
    g.set(30, 20, {"type": "roomexit", "args": ["basement", "stairup"], "kwargs": {"char": "stairdown"}})
    
    
    #g.set(45, 5, ["grass", "goblinspawner"])
    
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
    for x in range(40, 64):
        g.set(x, 18, "wall")
        g.set(x, 22, "wall")
    for x in range(40, 63):
        for y in range(19, 22):
            g.set(x, y, "ground")
    
    for y in range(19, 22):
        g.set(63, y, {"type": "roomexit", "args": ["arena"], "kwargs": {"char": "ground"}})
    
    g.set(30, 20, {"type": "roomexit", "args": ["begin", "stairdown"], "kwargs": {"char": "stairup"}})
    
    #g.set(22, 18, ["ground", "goblin"])
    d = g.toDict()
    d["spawn"] = (30, 20)
    d["places"] = {
        "stairup": (30, 20),
        "toarena": (63, 20)
        }
    return d

def generateArena():
    
    g = grid.Grid(64, 32, None)
    
    for x in range(10, 51):
        for y in range(10, 31):
            g.set(x, y, "wall")
    for x in range(11, 50):
        for y in range(11, 30):
            g.set(x, y, "ground")
    for x in range(0, 10):
        g.set(x, 18, "wall")
        g.set(x, 22, "wall")
    for x in range(1, 11):
        for y in range(19, 22):
            g.set(x, y, "ground")
    
    for y in range(19, 22):
        g.set(0, y, {"type": "roomexit", "args": ["basement", "toarena"], "kwargs": {"char": "ground"}})
    
    g.set(22, 14, ["ground", "goblinspawner"])
    g.set(40, 14, ["ground", "goblinspawner"])
    g.set(22, 26, ["ground", "goblinspawner"])
    g.set(40, 26, ["ground", "goblinspawner"])
    g.set(42, 20, ["ground", "goblinspawner"])
    
    d = g.toDict()
    d["spawn"] = (0, 20)
    return d


def generateWorld():
    worlddata = {
        "begin": "begin",
        "rooms":{
            "begin": generateBeginRoom(),
            "basement": generateBasement(),
            "arena": generateArena()
            }
        }
    
    #import json
    #with open("worlddata.json", "w") as f:
        #json.dump(worlddata, f, indent=2)
    return worlddata
