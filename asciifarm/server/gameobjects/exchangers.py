


from ..entity import Entity

from ..datacomponents import Static, Interact, Exchanger, Exchange

entities = {}


entities["trader"] = lambda: Entity(
    sprite="sign",
    name="trader",
    height=1,
    dataComponents=[
        Static("trader"),
        Interact,
        Exchanger([
            Exchange(["carrotseed"], ["radishes"], None, "buy_carrotseeds"),
            Exchange(["pebble"], ["radishes"], None, "buy_pebble")
        ], "Trade")
    ]
)
    

