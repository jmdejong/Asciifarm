import os.path
import json


def loadRoom(roomPath):
    with open(roomPath) as roomFile:
        room = json.load(roomFile)
    for name, pos in room["places"].items():
        room["places"][name] = tuple(pos)
    return room


def loadWorld(worldPath):
    
    with open(worldPath) as worldFile:
        world = json.load(worldFile)
    
    path = os.path.dirname(worldPath)
    
    for name, room in world["rooms"].items():
        if isinstance(room, str):
            world["rooms"][name] = loadRoom(os.path.join(path, room))
    
    return world
