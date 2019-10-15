

import random

from asciifarm.common import utils
from .. import gameobjects
from ..system import system
from ..datacomponents import Attackable, Input, StartTimer, Periodic, Equipment, Listen
from ..template import Template
from ..notification import AttackNotification, DamageNotification, KillNotification, HealNotification, DieNotification

@system([Attackable])
def attacked(obj, roomData, attackable):
    for type, strength, attacker in attackable.attacks:
        if type == "attack":
            defence = attackable.defence
            equipment = roomData.getComponent(obj, Equipment)
            if equipment is not None:
                defence += equipment.getBonus(roomData, "defence")
            damage = random.randint(0, int(100*strength / (defence + 100)))
        elif type == "heal":
            damage = -strength
        else:
            raise ValueError("Unknown attack type " + type)
        attackable.health -= damage
        attackable.health = utils.clamp(attackable.health, 0, attackable.maxHealth)
        
        # should this be it's own component? ('bleeding' for example)
        if damage > 0 and obj.getGround() is not None:
            wound = gameobjects.buildEntity(Template("wound", 4, obj.getHeight() - 0.01), roomData)
            wound.place(obj.getGround())
        
        
        _ear = roomData.getComponent(obj, Listen)
        ear = _ear.notifications if _ear is not None else []
        _attackear = roomData.getComponent(attacker, Listen)
        attackear = _attackear.notifications if _attackear is not None else []
        actor = attacker.name
        subject = obj.name
        
        if type == "attack":
            ear.append(DamageNotification(actor, subject, damage))
            attackear.append(AttackNotification(actor, subject, damage))
            input = roomData.getComponent(obj, Input)
            if input is not None:
                input.target = attacker # retaliation
        elif type == "heal":
            
            ear.append(HealNotification(actor, subject, -damage))
        
        if attackable.isDead():
            attackear.append(KillNotification(actor, subject))
            ear.append(DieNotification(actor, subject))
            for component in attackable.onDie:
                roomData.addComponent(obj, component)
            obj.remove()
    attackable.attacks = []

    


