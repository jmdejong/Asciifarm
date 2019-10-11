

from ..system import system
from ..datacomponents import Fighter, Attackable, Equipment

@system([Fighter])
def fight(obj, roomData, fighter):
    
    other = fighter.target
    if other is None:
        return
    otherFighter = roomData.getComponent(other, Attackable)
    if otherFighter is not None and fighter.inRange(obj, other) and fighter.attackReady < roomData.getStamp():
        strength = fighter.strength
        equipment = roomData.getComponent(obj, Equipment)
        if equipment is not None:
            strength += equipment.getBonus(roomData, "strength")
        otherFighter.attack(strength, obj)
        
        fighter.attackReady = roomData.getStamp() + fighter.slowness
    
    fighter.target = None

    
    


