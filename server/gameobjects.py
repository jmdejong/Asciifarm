

import random
import entity
from entity import Entity
from components.item import Item
from components.randomwalkcontroller import RandomWalkController
from components.move import Move
from components.portal import Portal
from components.trap import Trap
from components.fighter import Fighter
from components.faction import NEUTRAL, GOOD, EVIL
from components.monsterai import MonsterAi

def makeWall(roomEvents):
    return Entity(roomEvents, sprite="wall", height=2, solid=True)
    
def makeRock(roomEvents):
    return Entity(roomEvents, sprite="rock", height=10, solid=True)

def makeTree(roomEvents):
    return Entity(roomEvents, sprite="tree", height=3, solid=True)

def makeStone(roomEvents):
    return Entity(roomEvents, sprite="stone", height=0.2, components={"item": Item()})

def makePebble(roomEvents):
    return Entity(roomEvents, sprite="pebble", height=0.2, components={"item": Item()})

def makeGrass(roomEvents):
    return Entity(roomEvents, sprite=random.choice(["ground", "grass1", "grass2", "grass3"]), height=0.15)

def makeFloor(roomEvents):
    return Entity(roomEvents, sprite="floor", height=0.1)
    
def makeGround(roomEvents):
    return Entity(roomEvents, sprite="ground", height=0.1)
    
def makeWater(roomEvents):
    return Entity(roomEvents, sprite="water", height=0.1, solid=True)

def makeRoomExit(roomEvents, destRoom, destPos=None, char="exit", size=1):
    return Entity(roomEvents, sprite=char, height=size, components={"collision": Portal(destRoom, destPos)})

def makeRabbit(roomEvents):
    return Entity(roomEvents, sprite="rabbit", height=1, components={"move": Move(slowness=4), "controller": RandomWalkController(moveChance=0.05)})

def makeDummy(roomEvents):
    return Entity(roomEvents, sprite="dummy", height=1, components={"fighter": Fighter(maxHealth=20, strength=0), "alignment": EVIL})

def makeSpikeTrap(roomEvents):
    return Entity(roomEvents, sprite="spikes", height=1, components={"fighter": Fighter(maxHealth=25, strength=25), "collision": Trap()})

def makeGoblin(roomEvents):
    return Entity(roomEvents, sprite="goblin", height=1, components={"move": Move(slowness=4), "fighter": Fighter(maxHealth=25, strength=5, slowness=3), "alignment": EVIL, "controller": MonsterAi(viewDist=5, moveChance=0.01)})


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
    "spiketrap": makeSpikeTrap,
    "goblin": makeGoblin
    }
    

def makeEntity(entType, *args, **kwargs):
    return entitydict[entType](*args, **kwargs)
    
