
import random

from .. import pathfinding
from .. import faction
from ..system import System

@System("ai", "move")
def controlai(obj, roomData, ai, movable):
    alignment = obj.getComponent("alignment")
    
    fighter = obj.dataComponents.get("fighter")
    if fighter is not None:
        closestDistance = ai.viewDist + 1
        closest = None
        alignment = obj.dataComponents.get("faction", faction.NONE)
        for target in roomData.getTargets():
            distance = pathfinding.distanceBetween(obj, target)
            if (faction is None or alignment.isEnemy(target.dataComponents.get("faction", faction.NONE))) and distance < closestDistance:
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
        
