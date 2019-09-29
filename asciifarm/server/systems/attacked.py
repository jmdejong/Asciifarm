

import random

from asciifarm.common import utils
from .. import gameobjects

    
def attacked(obj, roomData):
    attackable = obj.dataComponents["attackable"]
    for type, strength, attacker in attackable.attacks:
        if type == "attack":
            defence = attackable.defence
            if obj.hasComponent("equipment"):
                defence += obj.getComponent("equipment").getBonus("defence")
            damage = random.randint(0, int(100*strength / (defence + 100)))
        elif type == "heal":
            damage = -strength
        else:
            raise ValueError("Unknown attack type " + type)
        attackable.health -= damage
        attackable.health = utils.clamp(attackable.health, 0, attackable.maxHealth)
        
        # should this be it's own component? ('bleeding' for example)
        if damage > 0 and obj.getGround() is not None:
            wound = gameobjects.makeEntity("wound", roomData, 4, obj.getHeight() - 0.01)
            wound.place(obj.getGround())
        
        if type == "attack":
            obj.trigger("damage", attacker, damage)
            attacker.trigger("attack", obj, damage)
        elif type == "heal":
            obj.trigger("heal", attacker, -damage)
        
        if attackable.isDead():
            obj.trigger("die", attacker)
            attacker.trigger("kill", obj)
            obj.remove()
    attackable.attacks = []
    


