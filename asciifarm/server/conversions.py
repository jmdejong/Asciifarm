

conversions = {
    "food": "eldritch_radish",
    "sword": "sword",
    "pebble": "pebble",
    "club": "club",
    "seed": "radishseed",
    "stone": "stone",
    "wall": "wall",
    "armour": "armour"
}

def convert(item):
    name = item["name"]
    if name in conversions:
        return conversions[name]
    raise ValueError("Unknow old object:", str(item))
