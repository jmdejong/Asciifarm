
from .component import Component
import random

class RandomWalkController(Component):
    
    def __init__(self, moveChance=1):
        self.moveChance = moveChance
    
    
    def attach(self, obj):
        self.owner = obj
        
        if not obj.dataComponents.get("move"):
            # todo: better exception
            raise Exception("Controller needs object with move component")
        
    
    
    def control(self):
        
        if random.random() < self.moveChance:
            direction = random.choice(["north", "south", "east", "west"])
            self.owner.dataComponents["move"].direction = direction
        
        
    def toJSON(self):
        return {
            "moveChance": self.moveChance
        }
