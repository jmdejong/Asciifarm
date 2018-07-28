

from . import gameobjects

class Exchange:
    
    
    def __init__(self, products, costs, description=None, name=None):
        self.products = products
        self.costs = costs
        if description is None:
            description = "{} ({})".format(", ".join(str(p) for p in products), ", ".join(str(c) for c in costs))
        self.description = description
        self.name = name or id(self)
        
    
    def perform(self, obj):
        inventory = obj.getComponent("inventory")
        if inventory is None:
            return
        costs = list(self.costs)
        toRemove = []
        for item in inventory.getItems():
            # get all the items to remove
            if item.name in costs:
                toRemove.append(item)
                costs.remove(item.name)
        if len(costs):
            # not all costs can be covered; other party can't afford trade
            return
        toAdd = [gameobjects.createEntity(product) for product in self.products]
        if not inventory.canAddAll(toAdd):
            return
        
        for item in toRemove:
            inventory.drop(item)
        
        for item in toAdd:
            inventory.add(item)
    
    def act(self, obj):
        self.perform(obj)
    
