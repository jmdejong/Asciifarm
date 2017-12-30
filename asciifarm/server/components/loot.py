import random
from .. import gameobjects
from .component import Component


class Loot(Component):
    """ entities that have this component will drop loot on death """
    
    def __init__(self, items):
        """ Items should be a list of tuples where the first element is the item name, and the second element the chance that that item gets dropped """
        
        self.items = items
    
    def attach(self, obj):
        
        self.owner = obj
        obj.addListener("die", self.dropLoot)
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData):
        self.roomData = roomData
    
    def dropLoot(self, obj, *data):
        for itemData in self.items:
            item = itemData[0]
            chance = 1
            args = []
            kwargs = {}
            if len(itemData) > 1:
                chance = itemData[1]
                if len(itemData) > 2:
                    args = itemData[2]
                    if len(itemData) > 3:
                        kwargs = itemData[3]
            
            if chance > random.random():
                obj = gameobjects.makeEntity(item, self.roomData, *args, preserve=True, **kwargs)
                obj.place(self.owner.getGround())
    
    def toJSON(self):
        return {"items": self.items}
