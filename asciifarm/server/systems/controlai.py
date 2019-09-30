
import random

from .. import pathfinding
from ..datacomponents import AI, Move, Fighter, Faction
from ..system import System

@System([AI, Move])
def controlai(obj, roomData, ai, movable):
    
    fighter = obj.getDataComponent(Fighter)
    if fighter is not None:
        closestDistance = ai.viewDist + 1
        closest = None
        alignment = obj.getDataComponent(Faction) or Faction.NONE
        for target in roomData.getTargets():
            distance = pathfinding.distanceBetween(obj, target)
            if (alignment.isEnemy(target.getDataComponent(Faction) or Faction.NONE)) and distance < closestDistance:
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
        
