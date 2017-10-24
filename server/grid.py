
import utils

class Grid:
    
    
    def __init__(self, width, height, default=0):
        self.width = width
        self.height = height
        self.clear(default)
    
    def clear(self, value):
        self.grid = [value for i in range(self.width*self.height)];
    
    def isValid(self, x, y):
        return x>=0 and y>=0 and x<self.width and y<self.height
    
    def get(self, x, y):
        if self.isValid(x, y):
            return self.grid[x+y*self.width]
        else:
            return None
    
    def set(self, x, y, value):
        if self.isValid(x, y):
            self.grid[x+y*self.width] = value
            return True
        else:
            return False
    
    
    def toString(self):
        return '\n'.join(
            ''.join(
                self.get(x, y) for x in range(self.width)
                ) for y in range(self.height)
            )
    
    def toDict(self):
        data = []
        valuesById = []
        idsByValue = {}
        #numIds = 0
        for char in self.grid:
            frozenChar = str(char)
            if frozenChar not in idsByValue:
                charId = len(valuesById) #numIds
                #numIds += 1
                valuesById.append(char)
                idsByValue[frozenChar] = charId
            charId = idsByValue[frozenChar]
            data.append(charId)
        return {
            "width": self.width,
            "height": self.height,
            "field": data,
            "mapping": valuesById
            }
    

def fromDict(data):
    width, height = data["width"], data["height"]
    field = data["field"] if "field" in data else utils.concat(data["grid"]) if "grid" in data else []
    mapping = data["mapping"] if "mapping" in data else {}
    grid = Grid(width, height)
    for (i, val) in enumerate(field):
        y, x = divmod(i, width)
        grid.set(x, y, mapping[val])
    
    return grid
