

class Selector:
    
    
    def __init__(self, inventory):
        self.value = 0
        self.inventory = inventory
    
    def getValue(self):
        return min(self.value, self.inventory.getNumItems()-1)
    
    def select(self, value, relative=False, modular=False):
        invLen = self.inventory.getNumItems()
        if relative:
            value += self.value
        if modular and invLen:
            value %= invLen
        if value < 0:
            value = 0
        if value >= invLen:
            value = invLen-1
        if value in range(invLen):
            self.value = value
            self.inventory.change()
