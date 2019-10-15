
from ..datacomponents import Input, Fighter, Move, Faction, Interact, Inventory, Equipment, Attackable, Item, UseMessage
from ..system import system
#from ..controls import MoveAction, TakeAction, DropAction, UseAction
from ..notification import SoundNotification

@system([Input, Fighter, Move])
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
    kind = action.name
    try:
        handler = handlers.get(kind)
    except TypeError:
        handler = None
    if handler is None:
        print("invalid action", action)
        return
    handler(obj, roomData, action)

def do_move(obj, roomData, action):
    direction = action.direction
    roomData.getComponent(obj, Move).direction = direction

def do_take(obj, roomData, action):
    rank = action.rank
    inventory = roomData.getComponent(obj, Inventory)
    if inventory is None or len(inventory.items) >= inventory.capacity:
        # can't take anything if there is no inventory or if it's full
        return
    objects = obj.getNearObjects()
    if rank is not None:
        if rank not in range(len(objects)):
            return
        objects = [objects[rank]]
    for item in objects:
        if roomData.getComponent(item, Item) is not None:
            inventory.add(item)
            obj.trigger("inventorychange")
            item.unPlace()
            break

def do_drop(obj, roomData, action):
    rank = action.rank
    inventory = roomData.getComponent(obj, Inventory)
    if inventory is None:
        return False
    if rank is None:
        rank = 0
    if rank not in range(len(inventory.items)):
        return False
    item = inventory.items[rank]
    inventory.items.remove(item)
    obj.trigger("inventorychange")
    item.place(obj.getGround())
    return True
    
def do_use(obj, roomData, action):
    rank = action.rank
    if action.container == "inventory":
        items = roomData.getComponent(obj, Inventory).items
    elif action.container == "equipment":
        items = [val for key, val in sorted(roomData.getComponent(obj, Equipment).slots.items())]
    if rank is None:
        rank = 0
    if rank not in range(len(items)):
        return
    item = items[rank]
    onUse = roomData.getComponent(item, Item).onUse
    for component in onUse:
        roomData.addComponent(item, component)
    roomData.addComponent(item, UseMessage(obj))

def do_interact(obj, roomData, action):
    directions = action.directions
    objects = _getNearbyObjects(obj, directions)
    for other in objects:
        if roomData.getComponent(other, Interact) is not None:
            for component in roomData.getComponent(other, Interact).components:
                roomData.addComponent(other, component)
            roomData.addComponent(other, UseMessage(obj, action.parameter))
            break

def do_attack(obj, roomData, action):
    directions = action.directions
    objects = _getNearbyObjects(obj, directions)
    if roomData.getComponent(obj, Input).target in objects:
        objects = {roomData.getComponent(obj, Input).target}
    fighter = roomData.getComponent(obj, Fighter)
    alignment = roomData.getComponent(obj, Faction) or Faction.NONE
    for other in objects:
        if fighter.inRange(obj, other) and alignment.isEnemy(roomData.getComponent(other, Faction) or Faction.NONE) and roomData.getComponent(other, Attackable):
            fighter.target = other
            roomData.getComponent(obj, Input).target = other
            break

def do_say(obj, roomData, action):
    text = action.text
    name = obj.name
    roomData.makeSound(SoundNotification(name, text))

def _getNearbyObjects(obj, directions):
    nearPlaces = obj.getGround().getNeighbours()
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
    "interact": do_interact,
    "attack": do_attack,
    "say": do_say
}

