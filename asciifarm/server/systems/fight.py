

from ..system import system

@system(["fighter"])
def fight(obj, roomData):
    fighter = obj.dataComponents["fighter"]
    
    other = fighter.target
    if other is None:
        return
    otherFighter = other.dataComponents.get("attackable")
    if otherFighter is not None and fighter.canAttack(obj, other) and fighter.attackReady < roomData.getStamp():
        strength = fighter.strength
        if obj.hasComponent("equipment"):
            strength += obj.getComponent("equipment").getBonus("strength")
        otherFighter.attack(strength, obj)
        
        fighter.attackReady = roomData.getStamp() + fighter.slowness
    
    fighter.target = None

    
    


