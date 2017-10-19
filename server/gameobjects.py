

import random
import entity
from entity import Entity
import components

def makeWall(roomEvents):
    return Entity(roomEvents, sprite="wall", height=2, solid=True)
    
def makeRock(roomEvents):
    return Entity(roomEvents, sprite="rock", height=10, solid=True)

def makeTree(roomEvents):
    return Entity(roomEvents, sprite="tree", height=3, solid=True)

def makeStone(roomEvents):
    return Entity(roomEvents, sprite="stone", height=0.2, solid=False, components={"item": components.Item()})

def makePebble(roomEvents):
    return Entity(roomEvents, sprite="pebble", height=0.2, solid=False, components={"item": components.Item()})

def makeGrass(roomEvents):
    return Entity(roomEvents, sprite=random.choice(["ground", "grass1", "grass2", "grass3"]), height=0.15, solid=False)

def makeFloor(roomEvents):
    return Entity(roomEvents, sprite="floor", height=0.1, solid=False)
    
def makeGround(roomEvents):
    return Entity(roomEvents, sprite="ground", height=0.1, solid=False)
    
def makeWater(roomEvents):
    return Entity(roomEvents, sprite="water", height=0.1, solid=True)

def makeRoomExit(roomEvents, destRoom, destPos=None, char="exit", size=1):
    return Entity(roomEvents, sprite=char, height=size, solid=False, components={"collision": components.Portal(destRoom, destPos)})



entitydict = {
    "wall": makeWall,
    "tree": makeTree,
    "stone": makeStone,
    "pebble": makePebble,
    "rock": makeRock,
    "grass": makeGrass,
    "water": makeWater,
    "floor": makeFloor,
    "ground": makeGround,
    "roomexit": makeRoomExit
    }
    

def makeEntity(entType, *args, **kwargs):
    return entitydict[entType](*args, **kwargs)
    
