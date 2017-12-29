

class Selector:
    
    
    def __init__(self, inventory):
        self.value = 0
        self.inventory = inventory
    
    def getValue(self):
        return min(self.value, self.inventory.getNumItems()-1)
    
    def select(self, value, relative=False):
        invLen = self.inventory.getNumItems()
        if relative:
            value += self.selector
        if value < 0:
            if not relative:
                value += invLen
            else:
                value = 0
        if value >= invLen:
            value = invLen-1
        if value in range(invLen):
            self.selector = value
            self.inventory.change()
