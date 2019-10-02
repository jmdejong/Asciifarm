


from ..entity import Entity
from ..exchange import Exchange

from ..datacomponents import Static
from ..components import OptionMenu
from ..components import Selectable

entities = {}


entities["trader"] = lambda: Entity(
    sprite="sign", height=1, components={
        "interact": Selectable(),
        "options": OptionMenu("Trade", [
            Exchange(["carrotseed"], ["radishes"], None, "buy_carrotseeds"),
            Exchange(["pebble"], ["radishes"], None, "buy_pebble")
        ])
    },
    dataComponents=[Static("trader")]
)
    

