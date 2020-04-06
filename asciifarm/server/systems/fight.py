

from ..system import system
from ..datacomponents import Fighter, Attackable, Equipment, Listen, Input
from ..template import Template
from .. import gameobjects
from ..notification import AttackNotification, DamageNotification, KillNotification, HealNotification, DieNotification

import random

@system([Fighter])
def fight(attacker, roomData, fighter):
    
    victim = fighter.target
    if victim is None:
        return
    attackable = roomData.getComponent(victim, Attackable)
    if attackable is not None and fighter.inRange(attacker, victim) and fighter.attackReady < roomData.getStamp():
        strength = fighter.strength
        equipment = roomData.getComponent(attacker, Equipment)
        if equipment is not None:
            strength += equipment.getBonus(roomData, "strength")
            
        defence = attackable.defence
        victimEquipment = roomData.getComponent(victim, Equipment)
        if victimEquipment is not None:
            defence += victimEquipment.getBonus(roomData, "defence")
        
        damage = random.randint(0, int(100*strength / (defence + 100)))
        #print("AA", victim.name, attackable.health, damage)
        attackable.health -= damage
        attackable.health = max(attackable.health, 0)
        #print("BB", victim.name, attackable.health, damage)
        
        if damage > 0 and victim.getGround() is not None:
            wound = gameobjects.buildEntity(Template("wound", 4, victim.getHeight() - 0.01), roomData)
            wound.place(victim.getGround())
        
        _victimear = roomData.getComponent(victim, Listen)
        victimear = _victimear.notifications if _victimear is not None else []
        _attackear = roomData.getComponent(attacker, Listen)
        attackear = _attackear.notifications if _attackear is not None else []
        actor = attacker.getName()
        subject = victim.getName()
        victimear.append(DamageNotification(actor, subject, damage))
        attackear.append(AttackNotification(actor, subject, damage))
        input = roomData.getComponent(victim, Input)
        if input is not None:
            input.target = attacker # retaliation
            
        if attackable.isDead():
            print(attackable.health, victim.name)
            attackear.append(KillNotification(actor, subject))
            victimear.append(DieNotification(actor, subject))
            for component in attackable.onDie:
                roomData.addComponent(victim, component)
            victim.remove()
        
        fighter.attackReady = roomData.getStamp() + fighter.slowness
    
    fighter.target = None

    
    


