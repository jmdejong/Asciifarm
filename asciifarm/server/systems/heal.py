

from ..system import system

@system(["heal", "attackable"])
def heal(obj, roomData):
    
    healing = obj.dataComponents["heal"]
    attackable = obj.dataComponents["attackable"]
    
    if not attackable.healthFull():
        if healing.nextHeal is not None and roomData.stepStamp > healing.nextHeal:
            attackable.heal(healing.amount, None)
            healing.nextHeal = roomData.getStamp() + healing.interval
        if healing.nextHeal is None:
            healing.nextHeal = roomData.getStamp() + healing.interval
