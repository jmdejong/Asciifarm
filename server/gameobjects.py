

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
from components.build import Build

""" This module contains factory functions for many placable entities, and a make function to call a factory by a string name """

entities = {}


def makeWall():
    return Entity(sprite="wall", height=2, solid=True)
entities["wall"] = makeWall

def makeRock():
    return Entity(sprite="rock", height=10, solid=True)
entities["rock"] = makeRock

def makeTree():
    return Entity(sprite="tree", height=3, solid=True)
entities["tree"] = makeTree

def makeStone():
    return Entity(sprite="stone", height=0.2, components={"item": Build("wall")})
entities["stone"] = makeStone

def makePebble():
    return Entity(sprite="pebble", height=0.2, components={"item": Item()})
entities["pebble"] = makePebble

def makeGrass():
    return Entity(sprite=random.choice(["ground", "grass1", "grass2", "grass3"]), height=0.1)
entities["grass"] = makeGrass

def makeFloor():
    return Entity(sprite="floor", height=0)
entities["floor"] = makeFloor
    
def makeGround():
    return Entity(sprite="ground", height=0)
entities["ground"] = makeGround
    
def makeWater():
    return Entity(sprite="water", height=0, solid=True)
entities["water"] = makeWater

def makeRoomExit(destRoom, destPos=None, char="exit", size=1):
    return Entity(sprite=char, height=size, components={"collision": Portal(destRoom, destPos)})
entities["roomexit"] = makeRoomExit

def makeRabbit():
    return Entity(sprite="rabbit", height=1, components={"move": Move(slowness=4), "controller": RandomWalkController(moveChance=0.05)})
entities["rabbit"] = makeRabbit

def makeDummy():
    return Entity(sprite="dummy", height=1, components={"fighter": Fighter(maxHealth=20, strength=0), "alignment": Alignment(faction.EVIL)})
entities["dummy"] = makeDummy

def makeSpikeTrap():
    return Entity(sprite="spikes", height=1, components={"fighter": Fighter(maxHealth=25, strength=25), "collision": Trap()})
entities["spiketrap"] = makeSpikeTrap

def makeGoblin():
    return Entity(sprite="goblin", height=1.2, components={
        "move": Move(slowness=4),
        "fighter": Fighter(maxHealth=25, strength=5, slowness=3),
        "alignment": Alignment(faction.EVIL),
        "controller": MonsterAi(viewDist=5, moveChance=0.01),
        "loot": Loot([("seed", .5), ("seed", .1)])
        })
entities["goblin"] = makeGoblin

def makeGoblinSpawner(): # I should probably generalize this...
    return Entity(sprite="portal", height=1, name="goblinspawner", components={"spawn": Spawner("goblin", 2, 20)})
entities["goblinspawner"] = makeGoblinSpawner

def makeSownSeed():
    return Entity(sprite="seed", height=0.05, components={"grow": Growing("youngplant", 100)})
entities["sownseed"] = makeSownSeed

def makeYoungPlant():
    return Entity(sprite="youngplant", height=0.5, components={"grow": Growing("plant", 200)})
entities["youngplant"] = makeYoungPlant

def makePlant():
    return Entity(sprite="plant", height=1.2)
entities["plant"] = makePlant


def makeSeed():
    return Entity(sprite="seed", height=0.3, components={"item": Build("sownseed")})
entities["seed"] = makeSeed


def makeEntity(entType, roomData, *args, **kwargs):
    entity = entities[entType](*args, **kwargs)
    entity.construct(roomData)
    return entity
    
