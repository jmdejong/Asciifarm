

def groundDistanceBetween(g1, g2):
    """ manhattan distance between two GroundPatch objects """
    x1, y1 = g1.getPos()
    x2, y2 = g2.getPos()
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return dx+dy

def distanceBetween(o1, o2):
    """ Manhattan distance between two enteties """
    return groundDistanceBetween(o1.getGround(), o2.getGround())



# todo: make this a generator.
def getObjsInRange(obj, dist=1):
    """ Get all objects within a given disance from the object (disance is inclusive)
    
    works similar to Breadth First Search
    the returned objects are sorted by distance from the initial object
    """
    nearPlaces = []
    ground = obj.getGround()
    frontier = [ground] # use as queue
    while len(frontier):
        place = frontier.pop(0)
        if place in nearPlaces or groundDistanceBetween(ground, place) > dist:
            continue
        nearPlaces.append(place)
        frontier += list(place.getNeighbours().values())
    nearObjs = []
    for place in nearPlaces:
        nearObjs += list(place.getObjs())
    return nearObjs


def directionsTo(start, target):
    """ the list of all directions from start that will be closer to target """
    x1, y1 = start.getGround().getPos()
    x2, y2 = target.getGround().getPos()
    directions = []
    if x2 < x1:
        directions.append("west")
    elif x2 > x1:
        directions.append("east")
    if y2 < y1:
        directions.append("north")
    elif y2 > y1:
        directions.append("south")
    
    return directions


def stepTo(start, target):
    """ a direction from start where the ground is accissible and that is closer to target"""
    neighbours = start.getGround().getNeighbours()
    for direction in directionsTo(start, target):
        if direction in neighbours and neighbours[direction].accessible():
            return direction
    return None




