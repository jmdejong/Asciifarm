

import gameobjects
import random

class Loot:
    """ entities that have this component will drop loot on death """
    
    def __init__(self, items):
        """ Items should be a list of tuples where the first element is the item name, and the second element the chance that that item gets dropped """
        
        self.items = items
    
    def attach(self, obj, roomData):
        
        self.owner = obj
        self.roomData = roomData
        obj.addListener(self.dropLoot)
    
    def dropLoot(self, obj, action, *data):
        if action == "die":
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
                    obj = gameobjects.makeEntity(item, self.roomData, *args, **kwargs)
                    obj.place(self.owner.getGround())
