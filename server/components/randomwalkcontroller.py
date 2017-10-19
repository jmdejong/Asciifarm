
import random

class RandomWalkController:
    
    def __init__(self, moveChance=1):
        self.moveChance = moveChance
    
    
    def attach(self, obj, events):
        self.owner = obj
        
        if not obj.getComponent("move"):
            # todo: better exception
            raise Exception("Controller needs object with move component")
        
        self.controlEvent = events["control"]
        self.controlEvent.addListener(self.control)
    
    
    def control(self, steps):
        
        if random.random() < self.moveChance:
            direction = random.choice(["north", "south", "east", "west"])
            self.owner.getComponent("move").move(direction)
        
    
    def remove(self):
        self.controlEvent.remove(self.control)
        
