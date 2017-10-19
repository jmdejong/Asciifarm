

import random
import entity
from entity import Entity
from components.item import Item
from components.randomwalkcontroller import RandomWalkController
from components.move import Move
from components.portal import Portal
from components.trap import Trap
from components.fighter import Fighter

def makeWall(roomEvents):
    return Entity(roomEvents, sprite="wall", height=2, solid=True)
    
def makeRock(roomEvents):
    return Entity(roomEvents, sprite="rock", height=10, solid=True)

def makeTree(roomEvents):
    return Entity(roomEvents, sprite="tree", height=3, solid=True)

def makeStone(roomEvents):
    return Entity(roomEvents, sprite="stone", height=0.2, solid=False, components={"item": Item()})

def makePebble(roomEvents):
    return Entity(roomEvents, sprite="pebble", height=0.2, solid=False, components={"item": Item()})

def makeGrass(roomEvents):
    return Entity(roomEvents, sprite=random.choice(["ground", "grass1", "grass2", "grass3"]), height=0.15, solid=False)

def makeFloor(roomEvents):
    return Entity(roomEvents, sprite="floor", height=0.1, solid=False)
    
def makeGround(roomEvents):
    return Entity(roomEvents, sprite="ground", height=0.1, solid=False)
    
def makeWater(roomEvents):
    return Entity(roomEvents, sprite="water", height=0.1, solid=True)

def makeRoomExit(roomEvents, destRoom, destPos=None, char="exit", size=1):
    return Entity(roomEvents, sprite=char, height=size, solid=False, components={"collision": Portal(destRoom, destPos)})

def makeRabbit(roomEvents):
    return Entity(roomEvents, sprite="rabbit", height=1, components={"move": Move(slowness=4), "controller": RandomWalkController(moveChance=0.05)})

def makeDummy(roomEvents):
    return Entity(roomEvents, sprite="dummy", height=1, components={"fighter": Fighter(health=20, strength=0)})

def makeSpikeTrap(roomEvents):
    return Entity(roomEvents, sprite="spikes", height=1, components={"fighter": Fighter(health=25, strength=25), "collision": Trap()})


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
    "roomexit": makeRoomExit,
    "rabbit": makeRabbit,
    "dummy": makeDummy,
    "spiketrap": makeSpikeTrap
    }
    

def makeEntity(entType, *args, **kwargs):
    return entitydict[entType](*args, **kwargs)
    
