
from .attackable import Attackable
from .fighter import Fighter
from .heal import Heal
from .move import Move
from .ai import AI
from .input import Input
from .faction import Faction
from .messages import Messages
from .loot import Loot


class Remove:
    pass

class Dead:
    pass


class Interact:
    
    def __init__(self, *components):
        self.components = list(components)
