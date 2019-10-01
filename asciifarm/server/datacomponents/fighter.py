
from ..pathfinding import distanceBetween
from .dc import DC

class Fighter(DC):
    
    def __init__(self, strength=0, slowness=1, range=1):
        self.strength = strength
        self.target = None
        self.slowness = slowness
        self.attackReady = 0
        self.range = range
    
    
    def inRange(self, owner, other):
        return distanceBetween(owner, other) <= self.range
