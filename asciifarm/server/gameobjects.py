import random

from . import entity
from . import faction
from .entity import Entity
from .components.item import Item
from .components.randomwalkcontroller import RandomWalkController
from .components.move import Move
from .components.portal import Portal
from .components.trap import Trap
from .components.fighter import Fighter
from .components.monsterai import MonsterAi
from .components.spawner import Spawner
from .components.grow import Growing
from .components.alignment import Alignment
from .components.loot import Loot
from .components.build import Build
from .components.harvest import Harvest
from .components.food import Food
from .components.equippable import Equippable
from .components.volatile import Volatile
from .components.change import Change
from .components.staticserializer import StaticSerializer as Static
from .components.customserializer import CustomSerializer as Custom

""" This module contains factory functions for many placable entities, and a make function to call a factory by a string name """

entities = {}

entities["wall"] = lambda: Entity(sprite="wall", height=2, flags={"solid"}, components={"serialize": Static("wall")})

entities["freeland"] = lambda: Entity(name="buildable", flags={"freeland"}, components={"serialize": Static("freeland")})

entities["rock"] = lambda: Entity(sprite="rock", height=10, flags={"solid"}, components={"serialize": Static("rock")})

entities["tree"] = lambda: Entity(sprite="tree", height=3, flags={"solid"}, components={"serialize": Static("tree")})

entities["house"] = lambda: Entity(sprite="house", height=3, flags={"solid"}, components={"serialize": Static("house")})

entities["fence"] = lambda: Entity(sprite="fence", height=1, flags={"solid"}, components={"serialize": Static("fence")})

entities["stone"] = lambda: Entity(sprite="stone", height=0.4, components={"item": Build("builtwall", flagsNeeded={"freeland"}, blockingFlags={"solid", "occupied"}), "serialize": Static("stone")})

entities["pebble"] = lambda: Entity(sprite="pebble", height=0.2, components={"item": Item(), "serialize": Static("pebble")})

entities["grass"] = lambda: Entity(
    sprite=random.choice(["ground"] + 2*["grass1", "grass2", "grass3"]), name="grass", height=0.1, flags={"floor", "soil"}, components={"serialize": Static("grass")})

entities["greengrass"] = lambda: Entity(
    sprite=random.choice(["grass1", "grass2", "grass3"]), height=0.1, flags={"floor", "soil"}, components={"serialize": Static("greengrass")})

entities["floor"] = lambda: Entity(sprite="floor", height=0.1, flags={"floor"}, components={"serialize": Static("floor")})

entities["ground"] = lambda: Entity(sprite="ground", height=0.1, flags={"floor", "soil"}, components={"serialize": Static("ground")})

entities["bridge"] = lambda small=False: Entity(sprite=("smallbridge" if small else "bridge"), height=0.1, flags={"floor"}, components={"serialize": Static("bridge", small)})

entities["water"] = lambda: Entity(sprite="water", height=0, components={"serialize": Static("water")})

entities["roomexit"] = lambda destRoom, destPos=None, mask=(False, False), sprite=" ", size=0: Entity(
    sprite=sprite, height=size, components={"collision": Portal(destRoom, destPos, mask), "serialize": Static(destRoom, destPos, mask, sprite, size)})

entities["rabbit"] = lambda: Entity(
    sprite="rabbit", name="bunny", height=1, components={"move": Move(slowness=4), "controller": RandomWalkController(moveChance=0.05), "serialize": Static("rabbit")})

entities["dummy"] = lambda: Entity(
    sprite="dummy", height=1, flags={"occupied"}, components={"fighter": Fighter(maxHealth=20, strength=0), "alignment": Alignment(faction.NONE)})

entities["spiketrap"] = lambda damage=25: Entity(
    sprite="spikes", height=1, flags={"occupied"}, components={"fighter": Fighter(maxHealth=25, strength=damage, attackable=False), "collision": Trap(), "serialize": Static("spiketrap")})

entities["goblin"] = lambda home=None: Entity(sprite="goblin", height=1.2, components={
        "move": Move(slowness=3),
        "fighter": Fighter(maxHealth=15, strength=5, slowness=8),
        "alignment": Alignment(faction.EVIL),
        "controller": MonsterAi(viewDist=8, moveChance=0.02, home=home),
        "loot": Loot([("sword", .05), ("club", .1), ("food", .25)])
        })

entities["troll"] = lambda home=None: Entity(sprite="troll", height=1.8, components={
        "move": Move(slowness=4),
        "fighter": Fighter(maxHealth=75, strength=15, slowness=10),
        "alignment": Alignment(faction.EVIL),
        "controller": MonsterAi(viewDist=8, moveChance=0.01, home=home),
        "loot": Loot([("stone", 1), ("stone", .3), ("pebble", .5), ("pebble", .5), ("pebble", .5)])
        })

entities["rat"] = lambda home=None: Entity(sprite="rat", height=1, components={
        "move": Move(slowness=3),
        "fighter": Fighter(maxHealth=8, strength=2, slowness=6),
        "alignment": Alignment(faction.EVIL),
        "controller": MonsterAi(viewDist=3, moveChance=0.08, home=home, homesickness=0.1),
        "loot": Loot([("seed", 0.9), ("seed", 0.3)])
        })

entities["spawner"] = lambda objType, number, delay, sprite=None, name=None, height=0, setHome=False, initialSpawn=True, objArgs=None, objKwargs=None: Entity(
    sprite=sprite, height=height, name=name, components={
        "spawn": Spawner(objType, number, delay, setHome, initialSpawn, objArgs, objKwargs),
        "serialize": Static("spawner", objType, number, delay, sprite, name, height, setHome, initialSpawn, objArgs, objKwargs)})

entities["sownseed"] = lambda: Entity(sprite="seed", height=0.05, name="plantedseed", flags={"occupied"}, components={"grow": Growing("youngplant", 100)})

entities["youngplant"] = lambda: Entity(sprite="youngplant", height=0.5, flags={"occupied"}, components={"grow": Growing("plant", 200)})

entities["plant"] = lambda: Entity(sprite="plant", height=1.2, flags={"occupied"}, components={
        "interact": Harvest(),
        "loot": Loot([("seed", .92), ("seed", .20), ("food", .8), ("food", .4)]),
        "serialize": Static("plant")
        })

entities["food"] = lambda: Entity(sprite="food", height=0.3, components={"item": Food(20), "serialize": Static("food")})

entities["seed"] = lambda: Entity(sprite="seed", height=0.2, components={"item": Build("sownseed", flagsNeeded={"soil"}, blockingFlags={"occupied", "solid"}), "serialize": Static("seed")})

entities["builtwall"] = lambda: Entity(
    sprite="wall", height=2, flags={"solid"}, components={
            "fighter": Fighter(maxHealth=100, strength=0),
            "alignment": Alignment(faction.NONE),
            "loot": Loot([("stone", 1)])})

entities["sword"] = lambda: Entity(sprite="sword", height=0.5, components={"item": Equippable("hand", {"strength": 5}), "serialize": Static("sword")})

entities["club"] = lambda: Entity(sprite="club", height=0.5, components={"item": Equippable("hand", {"strength": 3}), "serialize": Static("club")})

entities["weapon"] = lambda strength=0, name="weapon": Entity(sprite="sword", name=name, height=0.5, components={"item": Equippable("hand", {"strength": strength}), "serialize": Static("weapon", strength=strength)})

entities["armour"] = lambda: Entity(sprite="armour", height=0.5, components={"item": Equippable("body", {"defense": 100}), "serialize": Static("armour")})

entities["wound"] = lambda duration=4, height=0.2: Entity(sprite="wound", name="", height=height, components={"volatile": Volatile(duration), "serialize": Static(None)})

entities["closeddoor"] = lambda: Entity(sprite="closeddoor", name="door", height=2, flags={"solid"}, components={"interact": Change("opendoor"), "serialize": Static("closeddoor")})

entities["opendoor"] = lambda: Entity(sprite="opendoor", name="door", height=1, flags={"occupied"}, components={"interact": Change("closeddoor"), "serialize": Static("opendoor")})

#entities["builtcloseddoor"] = lambda health=None: Entity(sprite="closeddoor", name="door", height=2, flags={"solid"}, components={
    #"interact": Change(transferComponents={"fighter"}),
    #"fighter": Fighter(maxHealth=100, health=health, strength=0),
    #"alignment": Alignment(faction.NONE),
    #"loot": Loot([("hardwood", 1)])})

#entities["builtopendoor"] = lambda health=None: Entity(sprite="opendoor", name="door", height=1, flags={"occupied"}, components={
    #"interact": Change(),
    #"fighter": Fighter(maxHealth=100, health=health, strength=0),
    #"alignment": Alignment(faction.NONE),
    #"loot": Loot([("hardwood", 1)])})

entities["hardwood"] = lambda: Entity(sprite="hardwood", height=0.4, components={"item": Build("builtwall", flagsNeeded={"freeland"}, blockingFlags={"solid", "occupied"}), "serialize": Static(None)})

entities["engraved"] = lambda c: Entity(sprite="engravedwall-"+c, height=2, flags={"solid"}, components={"serialize": Static("wall", c)})

entities["letter"] = lambda c: Entity(sprite="emptyletter-"+c, components={"serialize": Static("letter", c)})

def makeEntity(entType, roomData, *args, preserve=False, **kwargs):
    entity = entities[entType](*args, **kwargs)
    entity.construct(roomData, preserve)
    return entity

def createEntity(data):
    obj = None
    if isinstance(data, str):
        obj = entities[data]()
    elif isinstance(data, dict):
        if "type" in data:
            obj = entities[data["type"]](*(data.get("args", [])), **(data.get("kwargs", {})))
        else:
            obj = entity.Entity.fromJSON(data)
    return obj

def buildEntity(data, roomData, preserve=False):
    obj = createEntity(data)
    if obj is not None:
        obj.construct(roomData, preserve)
    return obj
            
        
    
    
