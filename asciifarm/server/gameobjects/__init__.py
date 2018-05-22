

from ..entity import Entity

from .base import entities as base
from .crops import entities as crops
from .items import entities as items
from .misc import entities as misc
from .npcs import entities as npcs
from .structures import entities as structures

""" This module contains factory functions for many placable entities, and a make function to call a factory by a string name """

entities = {**base, **crops, **items, **misc, **npcs, **structures}


def makeEntity(entType, roomData, *args, preserve=False, **kwargs):
    entity = entities[entType](*args, **kwargs)
    entity.construct(roomData, preserve)
    return entity

def createEntity(data):
    obj = None
    if isinstance(data, str):
        obj = entities[data]()
    elif isinstance(data, dict):
        if "type" in data:
            obj = entities[data["type"]](*(data.get("args", [])), **(data.get("kwargs", {})))
        else:
            obj = Entity.fromJSON(data)
    return obj

def buildEntity(data, roomData, preserve=False):
    obj = createEntity(data)
    if obj is not None:
        obj.construct(roomData, preserve)
    return obj
            
        
    
    
