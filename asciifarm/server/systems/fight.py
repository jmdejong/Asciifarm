

from ..system import system
from ..datacomponents import Fighter, Attackable

@system([Fighter])
def fight(obj, roomData, fighter):
    
    other = fighter.target
    if other is None:
        return
    otherFighter = roomData.getComponent(other, Attackable)
    if otherFighter is not None and fighter.inRange(obj, other) and fighter.attackReady < roomData.getStamp():
        strength = fighter.strength
        if obj.hasComponent("equipment"):
            strength += obj.getComponent("equipment").getBonus("strength")
        otherFighter.attack(strength, obj)
        
        fighter.attackReady = roomData.getStamp() + fighter.slowness
    
    fighter.target = None

    
    


