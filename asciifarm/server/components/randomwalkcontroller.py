
from .component import Component
import random

class RandomWalkController(Component):
    
    def __init__(self, moveChance=1):
        self.moveChance = moveChance
    
    
    def attach(self, obj):
        self.owner = obj
        
        if not obj.getComponent("move"):
            # todo: better exception
            raise Exception("Controller needs object with move component")
        
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData):
        self.controlEvent = roomData.getEvent("control")
        self.controlEvent.addListener(self.control)
    
    
    def control(self):
        
        if random.random() < self.moveChance:
            direction = random.choice(["north", "south", "east", "west"])
            self.owner.getComponent("move").move(direction)
        
    
    def remove(self):
        self.controlEvent.removeListener(self.control)
        
    def toJSON(self):
        return {
            "moveChance": self.moveChance
        }
