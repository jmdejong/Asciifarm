
from ..entity import Entity
from ..components import StaticSerializer as Static
import random


entities = {}


entities["grass"] = lambda: Entity(
    sprite=random.choice(["ground"] + 2*["grass1", "grass2", "grass3"]), name="grass", height=0.1, flags={"floor", "soil"}, components={"serialize": Static("grass")})

entities["greengrass"] = lambda: Entity(
    sprite=random.choice(["grass1", "grass2", "grass3"]), height=0.1, flags={"floor", "soil"}, components={"serialize": Static("greengrass")})

entities["floor"] = lambda: Entity(sprite="floor", height=0.1, flags={"floor"}, components={"serialize": Static("floor")})

entities["ground"] = lambda: Entity(sprite="ground", height=0.1, flags={"floor", "soil"}, components={"serialize": Static("ground")})

entities["bridge"] = lambda small=False: Entity(sprite=("smallbridge" if small else "bridge"), height=0.1, flags={"floor"}, components={"serialize": Static("bridge", small)})

entities["water"] = lambda: Entity(sprite="water", height=0, components={"serialize": Static("water")})
