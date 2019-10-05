
import random

from ..system import system
from ..datacomponents import StartTimer, Periodic

@system([StartTimer, Periodic])
def checktimers(obj, roomData, _start, periodic):
    if periodic.targetTime is None:
        interval = periodic.interval
        if interval is None:
            raise ValueError("Neither interval nor targettime set for", str(obj), str(periodic))
        if periodic.randomise:
            interval = random.triangular(interval/2, interval*2, interval)
        periodic.targetTime = roomData.getStamp() + interval
    roomData.postpone(periodic.targetTime, obj, *periodic.components)
