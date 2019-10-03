
from ..system import system
from ..datacomponents import Waiting, Periodic

@system([Periodic], avoid=[Waiting])
def checktimers(obj, roomData, periodic):
    interval = periodic.interval
    if periodic.randomise:
        interval = random.triangular(interval/2, interval*2, interval)
    roomData.postpone(roomData.getStamp() + interval, obj, periodic.components)
