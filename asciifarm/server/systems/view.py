
from ..system import system
from ..datacomponents import Visible, Retina


changeActions = {
    "health": lambda p: ["health", p.getHealthPair()],
    "inventory": lambda p: ["inventory", [obj.getName() for obj in p.getInventory()]],
    "equipment": lambda p: ["equipment", sorted([(slot, (item.getName() if item else None)) for slot, item in p.getEquipment().items()])],
    "ground": lambda p: ["ground", [obj.getName() for obj in p.getGroundObjs() if obj.getName()]],
    "pos": lambda p: ["playerpos", p.getPos()],
    "selection": onSelectionChange
    }

@system([Retina])
def view(obj, roomData, retina):
    for action in changeActions:
        val = action(obj
    
