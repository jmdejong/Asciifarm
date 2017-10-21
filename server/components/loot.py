

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
            for item, chance in self.items:
                if chance > random.random():
                    # todo: args and kwargs
                    obj = gameobjects.makeEntity(item, self.roomData)
                    obj.place(self.owner.getGround())
