
from ..system import system
from ..datacomponents import Exchanger, Inventory, UseMessage, Listen, Remove
from ..template import Template
from .. import gameobjects

@system([UseMessage, Exchanger])
def exchange(obj, roomData, usemessages, exchanger):
    for use in usemessages:
        exchange = exchanger.options.get(use.parameter)
        if exchange is None:
            # give actor a list of options
            tell_options(obj, exchanger, roomData.getComponent(use.actor, Listen))
        else:
            # perform the exchange
            perform_exchange(exchange, roomData.getComponent(use.actor, Inventory), roomData)
            use.actor.trigger("inventorychange")


def tell_options(source, exchanger, ear):
    if ear is None:
        return
    if exchanger.description:
        ear.sounds.append((source, exchanger.description))
    for option in exchanger.options.values():
        ear.sounds.append((source, "{}: {}".format(option.name, option.description)))
    

def perform_exchange(exchange, inventory, roomData):
    if inventory is None:
        return
    costs = list(exchange.costs)
    toRemove = []
    for item in inventory.items:
        # get all the items to remove
        if item.name in costs:
            toRemove.append(item)
            costs.remove(item.name)
    if len(costs):
        # not all costs can be covered; other party can't afford trade
        return
    toAdd = [gameobjects.buildEntity(Template(product), roomData) for product in exchange.products]
    if len(inventory.items) - len(toRemove) + len(toAdd) > inventory.capacity:
        return
    
    for item in toRemove:
        inventory.items.remove(item)
        roomData.addComponent(item, Remove)
    for item in toAdd:
        inventory.add(item)
