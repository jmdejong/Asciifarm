

from ..entity import Entity

from .base import entities as base
from .crops import entities as crops
from .exchangers import entities as exchangers
from .items import entities as items
from .misc import entities as misc
from .npcs import entities as npcs
from .structures import entities as structures

""" This module contains factory functions for many placable entities, and a make function to call a factory by a string name """

entities = {**base, **crops, **items, **misc, **npcs, **structures, **exchangers}


def makeEntity(entType, roomData, *args, preserve=False, **kwargs):
    entity = entities[entType](*args, **kwargs)
    entity.construct(roomData, preserve)
    return entity

def createEntity(template):
    return entities[template.name](*template.args, **template.kwargs)

def buildEntity(template, roomData, preserve=False):
    obj = createEntity(template)
    if obj is not None:
        obj.construct(roomData, preserve)
    return obj
            
        
    
    
