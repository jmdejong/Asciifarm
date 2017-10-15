
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
                screen.set(x, y, room.getChar((x, y)))
        return screen.toDict()
    
    def roomView(self, roomName):
        room = self.world.getRoom(roomName)
        return self.viewRoom(room)
    
    def playerView(self, playerName):
        player = self.world.getPlayer(playerName)
        field = self.viewRoom(player.getRoom())
        #print(player.getRoom())
        holding = player.getInventory()
        data = {
            "type": "fullupdate",
            "info":{
                "holding": holding.char if holding else "nothing"
                #"ground": [obj.char for obj in player.ground.getObjs()]
            }
        }
        if field:
            data["field"] = field
        
        return data

def view(room):
    width = room.width
    height = room.height
    
    screen = grid.Grid(width, height)
    
    for x in range(width):
        for y in range(height):
            screen.set(x, y, room.getChar((x, y)))
    
    return screen
