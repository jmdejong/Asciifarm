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

""" This module contains factory functions for many placable entities, and a make function to call a factory by a string name """

entities = {}

entities["wall"] = lambda: Entity(sprite="wall", height=2, flags={"solid"})

entities["freeland"] = lambda: Entity(name="buildable", flags={"freeland"})

entities["rock"] = lambda: Entity(sprite="rock", height=10, flags={"solid"})

entities["tree"] = lambda: Entity(sprite="tree", height=3, flags={"solid"})

entities["house"] = lambda: Entity(sprite="house", height=3, flags={"solid"})

entities["fence"] = lambda: Entity(sprite="fence", height=1, flags={"solid"})

entities["stone"] = lambda: Entity(sprite="stone", height=0.4, components={"item": Build("builtwall", flagsNeeded={"freeland"}, blockingFlags={"solid", "occupied"})})

entities["pebble"] = lambda: Entity(sprite="pebble", height=0.2, components={"item": Item()})

entities["grass"] = lambda: Entity(
    sprite=random.choice(["ground"] + 2*["grass1", "grass2", "grass3"]), name="grass", height=0.1, flags={"floor", "soil"})

entities["greengrass"] = lambda: Entity(
    sprite=random.choice(["grass1", "grass2", "grass3"]), height=0.1, flags={"floor", "soil"})

entities["floor"] = lambda: Entity(sprite="floor", height=0.1, flags={"floor"})

entities["ground"] = lambda: Entity(sprite="ground", height=0.1, flags={"floor", "soil"})

entities["bridge"] = lambda small=False: Entity(sprite=("smallbridge" if small else "bridge"), height=0.1, flags={"floor"})

entities["water"] = lambda: Entity(sprite="water", height=0)

entities["roomexit"] = lambda destRoom, destPos=None, mask=(False, False), sprite=" ", size=0: Entity(
    sprite=sprite, height=size, components={"collision": Portal(destRoom, destPos, mask)})

entities["rabbit"] = lambda: Entity(
    sprite="rabbit", height=1, components={"move": Move(slowness=4), "controller": RandomWalkController(moveChance=0.05)})

entities["dummy"] = lambda: Entity(
    sprite="dummy", height=1, flags={"occupied"}, components={"fighter": Fighter(maxHealth=20, strength=0), "alignment": Alignment(faction.NONE)})

entities["spiketrap"] = lambda: Entity(
    sprite="spikes", height=1, flags={"occupied"}, components={"fighter": Fighter(maxHealth=25, strength=25), "collision": Trap()})

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
        "fighter": Fighter(maxHealth=8, strength=2, slowness=5),
        "alignment": Alignment(faction.EVIL),
        "controller": MonsterAi(viewDist=3, moveChance=0.08, home=home, homesickness=0.1),
        "loot": Loot([("seed", 0.9), ("seed", 0.3)])
        })

entities["spawner"] = lambda objType, number, delay, sprite=None, name=None, height=0, setHome=False, initialSpawn=False, objArgs=None, objKwargs=None: Entity(
    sprite=sprite, height=height, name=name, components={
        "spawn": Spawner(objType, number, delay, setHome, initialSpawn, objArgs, objKwargs)})

entities["sownseed"] = lambda: Entity(sprite="seed", height=0.05, name="plantedseed", flags={"occupied"}, components={"grow": Growing("youngplant", 100)})

entities["youngplant"] = lambda: Entity(sprite="youngplant", height=0.5, flags={"occupied"}, components={"grow": Growing("plant", 200)})

entities["plant"] = lambda: Entity(sprite="plant", height=1.2, flags={"occupied"}, components={
        "interact": Harvest(),
        "loot": Loot([("seed", .92), ("seed", .20), ("food", .8), ("food", .4)])
        })

entities["food"] = lambda: Entity(sprite="food", height=0.2, components={"item": Food(20)})

entities["seed"] = lambda: Entity(sprite="seed", height=0.3, components={"item": Build("sownseed", flagsNeeded={"soil"}, blockingFlags={"occupied", "solid"})})

entities["builtwall"] = lambda: Entity(
    sprite="wall", height=2, flags={"solid"}, components={
            "fighter": Fighter(maxHealth=100, strength=0),
            "alignment": Alignment(faction.NONE),
            "loot": Loot([("stone", 1)])})

entities["sword"] = lambda: Entity(sprite="sword", height=0.5, components={"item": Equippable("hand", {"strength": 5})})

entities["club"] = lambda: Entity(sprite="club", height=0.5, components={"item": Equippable("hand", {"strength": 3})})

entities["armour"] = lambda: Entity(sprite="armour", height=0.5, components={"item": Equippable("body", {"defense": 100})})

entities["wound"] = lambda duration=4, height=0.2: Entity(sprite="wound", height=height, components={"volatile": Volatile(duration)})

def makeEntity(entType, roomData, *args, preserve=False, **kwargs):
    entity = entities[entType](*args, **kwargs)
    entity.construct(roomData, preserve)
    return entity
    
