
from random import random as rand

class Loot:
    
    def __init__(self, items):
        self.items = []
        for itemData in items:
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
            self.items.append((item, chance, args, kwargs))
    
    def pick(self):
        return [(item, args, kwargs) for item, chance, args, kwargs in self.items if chance > rand()]
