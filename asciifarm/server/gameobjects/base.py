
from ..entity import Entity
from ..datacomponents import Static
import random


entities = {}


entities["grass"] = lambda: Entity(
    sprite=random.choice(["ground"] + 2*["grass1", "grass2", "grass3"]), name="grass", height=0.1, flags={"floor", "soil"}, dataComponents=[Static("grass")])

entities["greengrass"] = lambda: Entity(
    sprite=random.choice(["grass1", "grass2", "grass3"]), height=0.1, flags={"floor", "soil"}, dataComponents=[Static("greengrass")])

entities["floor"] = lambda: Entity(sprite="floor", height=0.1, flags={"floor"}, dataComponents=[Static("floor")])

entities["ground"] = lambda: Entity(sprite="ground", height=0.1, flags={"floor", "soil"}, dataComponents=[Static("ground")])

entities["bridge"] = lambda small=False: Entity(sprite=("smallbridge" if small else "bridge"), height=0.1, flags={"floor"}, dataComponents=[Static("bridge", small)])

entities["water"] = lambda: Entity(sprite="water", height=0, dataComponents=[Static("water")])
