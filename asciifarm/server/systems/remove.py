
from ..system import System
from ..datacomponents import ToRemove

@System(ToRemove)
def remove(obj, roomData, *_args):
    obj.doRemove()
