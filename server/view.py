
import grid

# this class extracts the data to send to the clients from the world


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
        room = self.world.getRoom(player.getRoom())
        data = [
            ["health", player.getHealth()],
            ["inventory", [obj.getSprite() for obj in player.getInventory()]],
            ["ground", [obj.getSprite() for obj in player.getGroundObjs()]],
            ["playerpos", player.getPos()]
            #"interactions": [ action + ' ' + obj.getChar() for action, obj in player.getInteractions()]
        ]
        if room:
            if player.shouldResetView():
                field = self.viewRoom(room)
                if field :
                    data.append(["field", field])
                    player.viewResetDone()
            changedCells = room.getChangedCells()
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
