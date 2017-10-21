

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
from components.spawner import Spawner
from components.grow import Growing


""" This module contains factory functions for many placable entities, and a make function to call a factory by a string name """

entities = {}


def makeWall(roomEvents):
    return Entity(roomEvents, sprite="wall", height=2, solid=True)
entities["wall"] = makeWall

def makeRock(roomEvents):
    return Entity(roomEvents, sprite="rock", height=10, solid=True)
entities["rock"] = makeRock

def makeTree(roomEvents):
    return Entity(roomEvents, sprite="tree", height=3, solid=True)
entities["tree"] = makeTree

def makeStone(roomEvents):
    return Entity(roomEvents, sprite="stone", height=0.2, components={"item": Item()})
entities["stone"] = makeStone

def makePebble(roomEvents):
    return Entity(roomEvents, sprite="pebble", height=0.2, components={"item": Item()})
entities["pebble"] = makePebble

def makeGrass(roomEvents):
    return Entity(roomEvents, sprite=random.choice(["ground", "grass1", "grass2", "grass3"]), height=0.15)
entities["grass"] = makeGrass

def makeFloor(roomEvents):
    return Entity(roomEvents, sprite="floor", height=0.1)
entities["floor"] = makeFloor
    
def makeGround(roomEvents):
    return Entity(roomEvents, sprite="ground", height=0.1)
entities["ground"] = makeGround
    
def makeWater(roomEvents):
    return Entity(roomEvents, sprite="water", height=0.1, solid=True)
entities["water"] = makeWater

def makeRoomExit(roomEvents, destRoom, destPos=None, char="exit", size=1):
    return Entity(roomEvents, sprite=char, height=size, components={"collision": Portal(destRoom, destPos)})
entities["roomexit"] = makeRoomExit

def makeRabbit(roomEvents):
    return Entity(roomEvents, sprite="rabbit", height=1, components={"move": Move(slowness=4), "controller": RandomWalkController(moveChance=0.05)})
entities["rabbit"] = makeRabbit

def makeDummy(roomEvents):
    return Entity(roomEvents, sprite="dummy", height=1, components={"fighter": Fighter(maxHealth=20, strength=0), "alignment": EVIL})
entities["dummy"] = makeDummy

def makeSpikeTrap(roomEvents):
    return Entity(roomEvents, sprite="spikes", height=1, components={"fighter": Fighter(maxHealth=25, strength=25), "collision": Trap()})
entities["spiketrap"] = makeSpikeTrap

def makeGoblin(roomEvents):
    return Entity(roomEvents, sprite="goblin", height=1.2, components={"move": Move(slowness=4), "fighter": Fighter(maxHealth=25, strength=5, slowness=3), "alignment": EVIL, "controller": MonsterAi(viewDist=5, moveChance=0.01)})
entities["goblin"] = makeGoblin

def makeGoblinSpawner(roomEvents): # I should probably generalize this...
    return Entity(roomEvents, sprite="portal", height=1, name="goblinspawner", components={"spawn": Spawner("goblin", 2, 20)})
entities["goblinspawner"] = makeGoblinSpawner

def makeSeed(roomEvents):
    return Entity(roomEvents, sprite="seed", height=0.3, components={"grow": Growing("plant", 100)})
entities["seed"] = makeSeed

def makePlant(roomEvents):
    return Entity(roomEvents, sprite="plant", height=1.2)
entities["plant"] = makePlant


def makeEntity(entType, *args, **kwargs):
    return entities[entType](*args, **kwargs)
    
