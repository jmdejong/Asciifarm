import random

from .. import pathfinding
from .component import Component


class MonsterAi(Component):
    
    
    def __init__(self, viewDist, moveChance=1, home=None, homesickness=0.05):
        self.moveChance = moveChance
        self.viewDist = viewDist
        self.home = home # Should home be a place instead of object? that would reduce references
        self.homesickness = homesickness
    
    
    def attach(self, obj):
        self.owner = obj
        
        for dep in {"move", "fighter", "alignment"}:
            if not (obj.getComponent(dep) or dep in obj.dataComponents):
                # todo: better exception
                raise Exception("Controller needs object with " + dep + " component")
            setattr(self, dep, obj.getComponent(dep))
        
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData, stamp):
        self.roomData = roomData
    
    
    def control(self):
        movable = self.owner.dataComponents["move"]
        fighter = self.owner.dataComponents["fighter"]
        
        if fighter:
            closestDistance = self.viewDist + 1
            closest = None
            for obj in self.roomData.getTargets():
                distance = pathfinding.distanceBetween(self.owner, obj)
                if self.alignment.isEnemy(obj) and distance < closestDistance:
                    closestDistance = distance
                    closest = obj
            if closest:
                if fighter.inRange(self.owner, closest):
                    fighter.target = closest
                else:
                    movable.direction = pathfinding.stepTo(self.owner, closest)
                return
        
        if random.random() < self.moveChance:
            if self.home and self.home.inRoom() and random.random() < (self.homesickness * pathfinding.distanceBetween(self.owner, self.home)):
                direction = pathfinding.stepTo(self.owner, self.home)
            else: 
                direction = random.choice(["north", "south", "east", "west"])
            movable.direction = direction
    
    
    def toJSON(self):
        return {
            "viewDist": self.viewDist,
            "moveChance": self.moveChance,
            "homesickness": self.homesickness
        } # home is not saved now ...

