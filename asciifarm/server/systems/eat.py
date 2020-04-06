
from ..system import system
from ..datacomponents import UseMessage, Food, Attackable, Remove, Inventory

@system([UseMessage, Food])
def eat(obj, roomData, use, food):
    actor = use[0].actor
    life = roomData.getComponent(actor, Attackable)
    if life is not None:
        newHealth = min(life.maxHealth, life.health + food.healing)
        life.health += food.healing
    roomData.addComponent(obj, Remove)
    inv = roomData.getComponent(actor, Inventory)
    if inv is not None:
        inv.items.remove(obj)
        inv.changed = True
    
