

import random
import entity
import faction
from entity import Entity
from components.item import Item
from components.randomwalkcontroller import RandomWalkController
from components.move import Move
from components.portal import Portal
from components.trap import Trap
from components.fighter import Fighter
from components.monsterai import MonsterAi
from components.spawner import Spawner
from components.grow import Growing
from components.alignment import Alignment
from components.loot import Loot

""" This module contains factory functions for many placable entities, and a make function to call a factory by a string name """

entities = {}


def makeWall(roomData):
    return Entity(roomData, sprite="wall", height=2, solid=True)
entities["wall"] = makeWall

def makeRock(roomData):
    return Entity(roomData, sprite="rock", height=10, solid=True)
entities["rock"] = makeRock

def makeTree(roomData):
    return Entity(roomData, sprite="tree", height=3, solid=True)
entities["tree"] = makeTree

def makeStone(roomData):
    return Entity(roomData, sprite="stone", height=0.2, components={"item": Item()})
entities["stone"] = makeStone

def makePebble(roomData):
    return Entity(roomData, sprite="pebble", height=0.2, components={"item": Item()})
entities["pebble"] = makePebble

def makeGrass(roomData):
    return Entity(roomData, sprite=random.choice(["ground", "grass1", "grass2", "grass3"]), height=0.15)
entities["grass"] = makeGrass

def makeFloor(roomData):
    return Entity(roomData, sprite="floor", height=0.1)
entities["floor"] = makeFloor
    
def makeGround(roomData):
    return Entity(roomData, sprite="ground", height=0.1)
entities["ground"] = makeGround
    
def makeWater(roomData):
    return Entity(roomData, sprite="water", height=0.1, solid=True)
entities["water"] = makeWater

def makeRoomExit(roomData, destRoom, destPos=None, char="exit", size=1):
    return Entity(roomData, sprite=char, height=size, components={"collision": Portal(destRoom, destPos)})
entities["roomexit"] = makeRoomExit

def makeRabbit(roomData):
    return Entity(roomData, sprite="rabbit", height=1, components={"move": Move(slowness=4), "controller": RandomWalkController(moveChance=0.05)})
entities["rabbit"] = makeRabbit

def makeDummy(roomData):
    return Entity(roomData, sprite="dummy", height=1, components={"fighter": Fighter(maxHealth=20, strength=0), "alignment": Alignment(faction.EVIL)})
entities["dummy"] = makeDummy

def makeSpikeTrap(roomData):
    return Entity(roomData, sprite="spikes", height=1, components={"fighter": Fighter(maxHealth=25, strength=25), "collision": Trap()})
entities["spiketrap"] = makeSpikeTrap

def makeGoblin(roomData):
    return Entity(roomData, sprite="goblin", height=1.2, components={
        "move": Move(slowness=4),
        "fighter": Fighter(maxHealth=25, strength=5, slowness=3),
        "alignment": Alignment(faction.EVIL),
        "controller": MonsterAi(viewDist=5, moveChance=0.01),
        "loot": Loot([("stone", .5), ("pebble", .5)])
        })
entities["goblin"] = makeGoblin

def makeGoblinSpawner(roomData): # I should probably generalize this...
    return Entity(roomData, sprite="portal", height=1, name="goblinspawner", components={"spawn": Spawner("goblin", 2, 20)})
entities["goblinspawner"] = makeGoblinSpawner

def makeSeed(roomData):
    return Entity(roomData, sprite="seed", height=0.3, components={"grow": Growing("plant", 100)})
entities["seed"] = makeSeed

def makePlant(roomData):
    return Entity(roomData, sprite="plant", height=1.2)
entities["plant"] = makePlant


def makeEntity(entType, *args, **kwargs):
    return entities[entType](*args, **kwargs)
    
