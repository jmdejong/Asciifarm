from . import grid

# this class extracts the data to send to the clients from the world

changeActions = {
    "health": lambda p: ["health", p.getHealth()],
    "inventory": lambda p: ["inventory", [obj.getSprite() for obj in p.getInventory()]],
    "ground": lambda p: ["ground", [obj.getName() for obj in p.getGroundObjs()]],
    "pos": lambda p: ["playerpos", p.getPos()]
    }

class View:
    
    def __init__(self, world):
        self.world = world
    
    
    def viewRoom(self, room):
        if not room:
            return None
        width = room.width
        height = room.height
        screen = grid.Grid(width, height)
        for x in range(width):
            for y in range(height):
                screen.set(x, y, room.getSprite((x, y)))
        return screen.toDict()
    
    def playerView(self, playerName):
        player = self.world.getPlayer(playerName)
        
        data = []
        changes = player.getChanges()
        player.resetChanges()
        if player.shouldResetView():
            changes |= {"health", "inventory", "ground", "pos"}
        for change in changes:
            if change in changeActions:
                data.append(changeActions[change](player))
        
        for message in player.readMessages():
            data.append(["message", message])
        
        room = self.world.getRoom(player.getRoom())
        if room:
            if player.shouldResetView():
                field = self.viewRoom(room)
                if field :
                    data.append(["field", field])
                    player.viewResetDone()
            changedCells = room.getChangedCells()
            if len(changedCells):
                data.append(["changecells", list(changedCells.items())])
        
        return data

def view(room):
    width = room.width
    height = room.height
    
    screen = grid.Grid(width, height)
    
    for x in range(width):
        for y in range(height):
            screen.set(x, y, room.getChar((x, y)))
    
    return screen
