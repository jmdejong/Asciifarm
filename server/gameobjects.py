

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
from components.harvest import Harvest
from components.food import Food

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
    return Entity(sprite="stone", height=0.4, components={"item": Build("builtwall")})
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

def makeRoomExit(destRoom, destPos=None, sprite="exit", size=1):
    return Entity(sprite=sprite, height=size, components={"collision": Portal(destRoom, destPos)})
entities["roomexit"] = makeRoomExit

def makeRabbit():
    return Entity(sprite="rabbit", height=1, components={"move": Move(slowness=4), "controller": RandomWalkController(moveChance=0.05)})
entities["rabbit"] = makeRabbit

def makeDummy():
    return Entity(sprite="dummy", height=1, components={"fighter": Fighter(maxHealth=20, strength=0), "alignment": Alignment(faction.NONE)})
entities["dummy"] = makeDummy

def makeSpikeTrap():
    return Entity(sprite="spikes", height=1, components={"fighter": Fighter(maxHealth=25, strength=25), "collision": Trap()})
entities["spiketrap"] = makeSpikeTrap

def makeGoblin():
    return Entity(sprite="goblin", height=1.2, components={
        "move": Move(slowness=3),
        "fighter": Fighter(maxHealth=25, strength=5, slowness=6),
        "alignment": Alignment(faction.EVIL),
        "controller": MonsterAi(viewDist=8, moveChance=0.01),
        "loot": Loot([("seed", .5), ("seed", .1)])
        })
entities["goblin"] = makeGoblin

def makeTroll():
    return Entity(sprite="troll", height=1.8, components={
        "move": Move(slowness=4),
        "fighter": Fighter(maxHealth=125, strength=12, slowness=10),
        "alignment": Alignment(faction.EVIL),
        "controller": MonsterAi(viewDist=8, moveChance=0.01),
        "loot": Loot([("stone", 1), ("stone", .3), ("pebble", .5), ("pebble", .5), ("pebble", .5)])
        })
entities["troll"] = makeTroll

def makeGoblinSpawner(): # I should probably generalize this...
    return Entity(sprite="portal", height=1, name="goblinspawner", components={"spawn": Spawner("goblin", 2, 20)})
entities["goblinspawner"] = makeGoblinSpawner

def makeSpawner(objType, number, delay, sprite="portal", name=None, objArgs=[], objKwargs={}):
    return Entity(sprite=sprite, height=1, name=name, components={"spawn": Spawner(objType, number, delay, objArgs, objKwargs)})
entities["spawner"] = makeSpawner

def makeSownSeed():
    return Entity(sprite="seed", height=0.05, name="plantedseed", components={"grow": Growing("youngplant", 100)})
entities["sownseed"] = makeSownSeed

def makeYoungPlant():
    return Entity(sprite="youngplant", height=0.5, components={"grow": Growing("plant", 200)})
entities["youngplant"] = makeYoungPlant

def makePlant():
    return Entity(sprite="plant", height=1.2, components={
        "interact": Harvest(),
        "loot": Loot([("seed", .92), ("seed", .20), ("food", .8), ("food", .4)])
        })
entities["plant"] = makePlant

def makeFood():
    return Entity(sprite="food", height=0.2, components={"item": Food(20)})
entities["food"] = makeFood


def makeSeed():
    return Entity(sprite="seed", height=0.3, components={"item": Build("sownseed")})
entities["seed"] = makeSeed


def makeBuiltWall():
    return Entity(sprite="wall", height=2, solid=True, components={"fighter": Fighter(maxHealth=100, strength=0), "alignment": Alignment(faction.NONE), "loot": Loot([("stone", 1)])})
entities["builtwall"] = makeBuiltWall


def makeEntity(entType, roomData, *args, **kwargs):
    entity = entities[entType](*args, **kwargs)
    entity.construct(roomData)
    return entity
    
