

from placable import GameObject
import playerent
import random

class Wall(GameObject):
    
    char = 'wall'
    size = 2
    attributes = {
        "solid",
        }


class Rock(GameObject):
    
    char = 'rock'
    size = 10
    attributes = {
        "solid",
        }
    


class Tree(GameObject):
    
    char = 'tree'# 🌳♣♠𐇲𐂷
    size = 3
    attributes = {
        "solid",
        }


class Stone(GameObject):
    
    char = 'stone' # •
    size = 0.2
    attributes = {
        "takable",
        }


class Grass(GameObject):
    
    size = 0.15
    
    def __init__(self, *args):
        self.char = random.choice(["ground", "grass1", "grass2", "grass3"])

class Floor(GameObject):
    
    char = "floor"
    size = 0.1

class Ground(GameObject):
    
    char = "ground"
    size = 0.1

class Water(GameObject):
    
    char = "water"
    size = 0.1
    attributes = {
        "solid"
        }


#class MapExit(GameObject):
    
    #char = "$"
    
    #def __init__(self)

## not really compatible yet
#class Rabbit(GameObject):
    
    #char = 'rabbit'
    #size = 2
    #direction = None
    #attributes = {}
    #slowness = 8
    
    #def __init__(self, x, y, field, game, name=None):
        #self.controller = {}
        #self.game = game
        #self.name = name or str(id(self))
        #self.x = x
        #self.y = y
        #self.ground = None
        #self.field = field
        #self.place(x, y)
        #self.holding = None
        #self.moveCooldown = random.randrange(self.slowness)
        #game.addUpdateListener(self.update, self)
    
    
    #def place(self, x, y):
        #if self.field:
            #self.field.removeObj(self.x, self.y, self)
            #self.field.addObj(x, y, self)
            #self.ground = self.field.get(x,y)
        #self.x = x
        #self.y = y
            
    
    #def update(self):
        #self.moveCooldown = max(self.moveCooldown-1, 0)
        
        #action = random.choice(["north", "east", "south", "west", "", "", "", ""])
        #if action in {"north", "east", "south", "west"} and self.moveCooldown <= 0:
            #direction = action
            #dx = (direction == "east") - (direction == "west")
            #dy = (direction == "south") - (direction == "north")
            
            #newx = self.x + dx
            #newy = self.y + dy
            
            #if self.field.get(newx, newy).accesible():
                #self.place(newx, newy)
                #self.moveCooldown = self.slowness
            
            
    
    #def remove(self):
        ##self.game.removePlayer(self.name)
        #self.field.removeObj(self.x, self.y, self)
        #self.game.removeUpdateListener(self)
        



    



objectdict = {
    "wall": Wall,
    "tree": Tree,
    "player": playerent.Player,
    "stone": Stone,
    "rock": Rock,
    "rabbit": Rabbit,
    "grass": Grass,
    "water": Water,
    "floor": Floor,
    "ground": Ground
    }


def makeObject(name, *args, **kwargs):
    return objectdict[name](*args, **kwargs)
