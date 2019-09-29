
import random

from .. import pathfinding

def controlai(obj, roomData):
    movable = obj.dataComponents["move"]
    ai = obj.dataComponents["ai"]
    alignment = obj.getComponent("alignment")
    
    fighter = obj.dataComponents.get("fighter")
    if fighter is not None:
        closestDistance = ai.viewDist + 1
        closest = None
        for target in roomData.getTargets():
            distance = pathfinding.distanceBetween(obj, target)
            if alignment.isEnemy(target) and distance < closestDistance:
                closestDistance = distance
                closest = target
        if closest:
            if fighter.inRange(obj, closest):
                fighter.target = closest
            else:
                movable.direction = pathfinding.stepTo(obj, closest)
            return
    
    if random.random() < ai.moveChance:
        if ai.home and ai.home.inRoom() and random.random() < (ai.homesickness * pathfinding.distanceBetween(obj, ai.home)):
            direction = pathfinding.stepTo(obj, ai.home)
        else: 
            direction = random.choice(["north", "south", "east", "west"])
        movable.direction = direction
