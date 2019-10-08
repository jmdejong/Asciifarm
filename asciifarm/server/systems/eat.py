
from ..system import system
from ..datacomponents import UseMessage, Food, Attackable, Remove, Inventory

@system([UseMessage, Food])
def eat(obj, roomData, use, food):
    actor = use[0].actor
    life = roomData.getComponent(actor, Attackable)
    if life is not None:
        life.heal(food.healing, obj)
    roomData.addComponent(obj, Remove)
    inv = roomData.getComponent(actor, Inventory)
    if inv is not None:
        inv.items.remove(obj)
        actor.trigger("inventorychange")
    
