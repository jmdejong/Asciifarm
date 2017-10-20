
import pathfinding
import random


class MonsterAi:
    
    
    def __init__(self, viewDist, moveChance=1):
        self.moveChance = moveChance
        self.viewdist = viewDist
    
    
    def attach(self, obj, events):
        self.owner = obj
        
        for dep in {"move", "fighter", "alignment"}:
            if not obj.getComponent(dep):
                # todo: better exception
                raise Exception("Controller needs object with " + dep + " component")
            
            setattr(self, dep, obj.getComponent(dep))
        
        self.controlEvent = events["control"]
        self.controlEvent.addListener(self.control)
    
    
    def control(self):
        #print("controlling monstar")
        for obj in pathfinding.getObjsInRange(self.owner, self.viewdist):
            if self.alignment.isEnemy(obj):
                # this is now the closest enemy
                
                if pathfinding.distanceBetween(self.owner, obj) < 2:
                    self.fighter.attack(obj)
                else:
                    self.move.move(pathfinding.stepTo(self.owner, obj))
                break
        else:
            if random.random() < self.moveChance:
                direction = random.choice(["north", "south", "east", "west"])
                self.move.move(direction)
        
    
    def remove(self):
        self.controlEvent.removeListener(self.control)

