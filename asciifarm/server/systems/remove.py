
from ..system import system
from ..datacomponents import Remove

@system([Remove])
def remove(obj, roomData, *_args):
    obj.doRemove()
