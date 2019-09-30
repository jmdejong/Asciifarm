
from .attackable import Attackable
from .fighter import Fighter
from .heal import Heal
from .move import Move
from .ai import AI
from .input import Input
from .faction import Faction
from .events import Events
from .loot import Loot
from .inbox import Inbox
from .portal import Portal


class Remove:
    pass

class Dead:
    pass


class Interact:
    
    def __init__(self, *components):
        self.components = list(components)

class Trap:
    pass
