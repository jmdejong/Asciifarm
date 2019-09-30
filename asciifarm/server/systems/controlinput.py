
from ..datacomponents import Input, Fighter, Move, Faction
from ..system import System

@System([Input, Fighter, Move])
def control(obj, roomData, input, fighter, *_args):
    action = input.action
    if action:
        input.target = None
    input.action = None
    if action is not None:
        executeAction(obj, roomData, action)
    if input.target:
        fighter.target = input.target

def executeAction(obj, roomData, action):
    
    kind = action[0]
    if len(action) > 1:
        arg = action[1]
    else:
        arg = None
    try:
        handler = handlers.get(kind)
    except TypeError:
        handler = None
    if handler is None:
        print("invalid action", action)
        return
    handler(obj, roomData, arg)

def do_move(obj, roomData, direction):
    if direction not in {"north", "south", "east", "west"}:
        return
    obj.getDataComponent(Move).direction = direction

def do_take(obj, roomData, rank):
    objects = obj.getNearObjects()
    if rank is not None:
        if rank not in range(len(objects)):
            return
        objects = [objects[rank]]
    for item in objects:
        if item.getComponent("item") is not None and obj.getComponent("inventory").canAdd(item):
            obj.trigger("take", item)
            item.remove()
            break

def do_drop(obj, roomData, rank):
    items = obj.getComponent("inventory").getItems()
    if rank is None:
        rank = 0
    if rank not in range(len(items)):
        return False
    item = items[rank]
    obj.getComponent("inventory").drop(item)
    item.construct(roomData, preserve=True)
    item.place(obj.getGround())
    return True
    
def do_use(obj, roomData, rank):
    items = obj.getComponent("inventory").getItems()
    if rank is None:
        rank = 0
    if rank not in range(len(items)):
        return
    item = items[rank]
    item.getComponent("item").use(obj)

def do_unequip(obj, roomData, rank):
    slots = sorted(obj.getComponent("equipment").getSlots().items())
    if rank is not None:
        if rank not in range(len(slots)):
            return
        slots = [slots[rank]]
    for (slot, item) in slots:
        if item is not None and obj.getComponent("inventory").canAdd(item):
            obj.getComponent("equipment").unEquip(slot)
            obj.trigger("take", item)

def do_interact(obj, roomData, directions):
    objects = _getNearbyObjects(obj, directions)
    for other in objects:
        if other.getComponent("interact") is not None:
            other.getComponent("interact").interact(obj)
            break

def do_attack(obj, roomData, directions):
    objects = _getNearbyObjects(obj, directions)
    if obj.getDataComponent(Input).target in objects:
        objects = {obj.getDataComponent(Input).target}
    fighter = obj.getDataComponent(Fighter)
    alignment = obj.getDataComponent(Faction) or Faction.NONE
    for other in objects:
        if fighter.inRange(obj, other) and alignment.isEnemy(other.getDataComponent(Faction) or Faction.NONE):
            fighter.target = other
            obj.getDataComponent(Input).target = other
            break

def do_say(obj, roomData, text):
    if type(text) != str:
        return
    roomData.getEvent("sound").trigger(obj, text)

def do_pick(obj, roomData, option):
    selected = obj.getComponent("select").getSelected()
    if selected is None:
        return
    optionmenu = selected.getComponent("options")
    if optionmenu is None:
        return
    optionmenu.choose(option, obj)

def _getNearbyObjects(obj, directions):
    nearPlaces = obj.getGround().getNeighbours()
    if not isinstance(directions, list):
        directions = [directions]
    objects = []
    for direction in directions:
        if direction is None:
            objects += obj.getNearObjects()
        elif isinstance(direction, str) and direction in nearPlaces:
            objects += nearPlaces[direction].getObjs()
    return objects
    

handlers = {
    "move": do_move,
    "take": do_take,
    "drop": do_drop,
    "use": do_use,
    "unequip": do_unequip,
    "interact": do_interact,
    "attack": do_attack,
    "say": do_say,
    "pick": do_pick
}

