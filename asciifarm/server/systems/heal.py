

from ..system import system
from ..datacomponents import Heal, Attackable, Listen
from ..notification import HealNotification

@system([Heal, Attackable])
def heal(obj, roomData, healing, attackable):
    
    if not attackable.healthFull():
        if healing.nextHeal is not None and roomData.stepStamp > healing.nextHeal:
            oldhealth = attackable.health
            attackable.health = max(attackable.health, min(attackable.health + healing.amount, attackable.maxHealth))
            #ear = roomData.getComponent(obj, Listen)
            #if ear is not None:
                #difference = attackable.health - oldhealth
                #if difference > 0:
                    #ear.notifications.append(HealNotification(None, obj.name, difference))
            healing.nextHeal = roomData.getStamp() + healing.interval
        if healing.nextHeal is None:
            healing.nextHeal = roomData.getStamp() + healing.interval
