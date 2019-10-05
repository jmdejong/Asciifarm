
import random

from .. import pathfinding
from ..datacomponents import AI, Move, Fighter, Faction, Attackable, Home
from ..system import system

@system([AI, Move])
def controlai(obj, roomData, ai, movable):
    
    fighter = roomData.getComponent(obj, Fighter)
    if fighter is not None:
        closestDistance = ai.viewDist + 1
        closest = None
        alignment = roomData.getComponent(obj, Faction) or Faction.NONE
        for target in roomData.dataComponents[Attackable]:
            distance = pathfinding.distanceBetween(obj, target)
            if (alignment.isEnemy(roomData.getComponent(target, Faction) or Faction.NONE)) and distance < closestDistance:
                closestDistance = distance
                closest = target
        if closest:
            if fighter.inRange(obj, closest):
                fighter.target = closest
            else:
                movable.direction = pathfinding.stepTo(obj, closest)
            return
    
    if random.random() < ai.moveChance:
        home = roomData.getComponent(obj, Home)
        if home is not None and home.home.inRoom() and random.random() < (ai.homesickness * pathfinding.distanceBetween(obj, home.home)):
            direction = pathfinding.stepTo(obj, home.home)
        else: 
            direction = random.choice(["north", "south", "east", "west"])
        movable.direction = direction
        
