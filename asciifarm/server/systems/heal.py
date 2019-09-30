

from ..system import System
from ..datacomponents import Heal, Attackable

@System([Heal, Attackable])
def heal(obj, roomData, healing, attackable):
    
    if not attackable.healthFull():
        if healing.nextHeal is not None and roomData.stepStamp > healing.nextHeal:
            attackable.heal(healing.amount, None)
            healing.nextHeal = roomData.getStamp() + healing.interval
        if healing.nextHeal is None:
            healing.nextHeal = roomData.getStamp() + healing.interval
