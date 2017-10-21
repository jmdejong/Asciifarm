
import pathfinding
import random


class MonsterAi:
    
    
    def __init__(self, viewDist, moveChance=1):
        self.moveChance = moveChance
        self.viewDist = viewDist
    
    
    def attach(self, obj, roomData):
        self.owner = obj
        
        for dep in {"move", "fighter", "alignment"}:
            if not obj.getComponent(dep):
                # todo: better exception
                raise Exception("Controller needs object with " + dep + " component")
            
            setattr(self, dep, obj.getComponent(dep))
        
        self.controlEvent = roomData.getEvent("control")
        self.controlEvent.addListener(self.control)
        self.roomData = roomData
    
    
    def control(self):
        closestDistance = self.viewDist + 1
        closest = None
        for obj in self.roomData.getTargets():
            distance = pathfinding.distanceBetween(self.owner, obj)
            if self.alignment.isEnemy(obj) and distance < closestDistance:
                closestDistance = distance
                closest = obj
        if closest:
            if pathfinding.distanceBetween(self.owner, closest) <= 1:
                self.fighter.attack(closest)
            else:
                self.move.move(pathfinding.stepTo(self.owner, closest))
        else:
            if random.random() < self.moveChance:
                direction = random.choice(["north", "south", "east", "west"])
                self.move.move(direction)
    
    def remove(self):
        self.controlEvent.removeListener(self.control)

