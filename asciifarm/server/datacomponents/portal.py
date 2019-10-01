
from .dc import DC

class Portal(DC):
    
    def __init__(self, destRoom, destPos=None, mask=(False, False)):
        self.destRoom = destRoom
        self.origin = destPos
        self.mask = mask
    

