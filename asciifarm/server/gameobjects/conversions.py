

conversions = {
    "food": "eldritch_radish",
    "sword": "sword",
    "godsword": {"type": "weapon", "kwargs": {"strength": 500, "name": "godsword"}},
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
    raise ValueError("Unknown old object:", str(item))
