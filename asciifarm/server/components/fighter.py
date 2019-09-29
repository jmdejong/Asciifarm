
from asciifarm.common import utils
from .component import Component
from .. import gameobjects
from ..pathfinding import distanceBetween


class FighterData:
    
    
    
    def __init__(self, strength=0, slowness=1, range=1):
        self.strength = strength
        self.target = None
        self.slowness = slowness
        self.attackReady = 0
        self.range = range
    
    
    def inRange(self, owner, other):
        return distanceBetween(owner, other) <= self.range
    
    def canAttack(self, owner, other):
        return self.inRange(owner, other) and other.dataComponents.get("attackable")
    

