
from ..system import System
from ..datacomponents import Remove

@System([Remove])
def remove(obj, roomData, *_args):
    obj.doRemove()
