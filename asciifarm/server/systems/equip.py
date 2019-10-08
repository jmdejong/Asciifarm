
from ..system import system
from ..datacomponents import UseMessage, Equippable, Equipment, Inventory

@system([UseMessage, Equippable])
def equip(obj, roomData, use, equippable):
    actor = use[0].actor
    equipment = roomData.getComponent(actor, Equipment)
    inv = roomData.getComponent(actor, Inventory)
    if equipment is None or equippable.slot not in equipment.slots or inv is None:
        raise Exception("attempting to equip whithout having inventory", equippable.slot, str(equipment.slots))
    if obj in inv.items:
        
        inv.items.remove(obj)
        olditem = equipment.slots[equippable.slot]
        if olditem is not None:
            inv.add(olditem)
        equipment.slots[equippable.slot] = obj
    elif equipment.slots[equippable.slot] == obj:
        if len(inventory.items) < capacity:
            equipment.slots[equippable.slot] = None
            inventory.add(obj)
    else:
        raise Exception("attempting to equip item not in inventory")
    actor.trigger("inventorychange")
    actor.trigger("equipmentchange")
    
