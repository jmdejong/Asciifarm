
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
from .periodic import Periodic
from .equipment import Equipment
from .spawner import Spawner
from .item import Item
from .held import Held

from .messages import Message, EnterMessage, LootMessage, StartTimer, Create, SpawnMessage, EatMessage

class Remove:
    pass

class Dead:
    pass


class Interact:
    
    def __init__(self, *components):
        self.components = list(components)

class Trap:
    pass

class Home:
    def __init__(self, home):
        self.home = home
