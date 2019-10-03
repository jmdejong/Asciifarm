
from .attackable import Attackable
from .fighter import Fighter
from .heal import Heal
from .move import Move
from .ai import AI
from .input import Input
from .faction import Faction
from .events import Events
from .loot import Loot
from .portal import Portal
from .dc import DC
from .serialise import Serialise, Static
from .inventory import Inventory
from .listen import Listen

from .messages import Message, EnterMessage, LootMessage

class Remove(DC):
    pass

class Dead(DC):
    pass


class Interact(DC):
    
    def __init__(self, *components):
        self.components = list(components)

class Trap(DC):
    pass
