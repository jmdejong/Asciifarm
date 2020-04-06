from . import grid

# this class extracts the data to send to the clients from the world

viewActions = {
    "health": lambda p: ["health", p.getHealthPair()],
    "inventory": lambda p: ["inventory", [obj.getName() for obj in p.getInventory()]],
    "equipment": lambda p: ["equipment", sorted([(slot, (item.getName() if item else None)) for slot, item in p.getEquipment().items()])],
    "ground": lambda p: ["ground", [obj.getName() for obj in p.getGroundObjs() if obj.getName()]],
    "pos": lambda p: ["playerpos", p.getPos()]
    }

class View:
    
    def __init__(self, world):
        self.world = world
        self.retinas = {}
    
    
    def viewRoom(self, room):
        if not room:
            return None
        width = room.width
        height = room.height
        screen = grid.Grid(width, height)
        for x in range(width):
            for y in range(height):
                screen.set(x, y, room.getSprites((x, y)))
        return screen.toDict()
    
    def playerView(self, playerName):
        player = self.world.getPlayer(playerName)
        if player is None:
            return None
        if player not in self.retinas:
            self.retinas[player] = {}
        
        data = []
        for message in player.readMessages():
            data.append(["message", message.toJSON()])
        
        #changes = player.readChanges()
        #if player.shouldResetView():
            #changes |= {"health", "inventory", "ground", "equipment", "pos"}
        for name, action in viewActions.items():
            val = action(player)
            if val is None or val == self.retinas[player].get(name):
                continue
            self.retinas[player][name] = val
            data.append(val)
            #if change in changeActions:
                #val = changeActions[change](player)
                #if val is not None and val[1] is not None:
                    #data.append(val)
        
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

