
from asciifarm.common import utils


class ListSelector:
    
    def __init__(self, widget):
        self.widget = widget
        self.items = []
        self.selector = 0
    
    def getSelected(self):
        return self.selector
    
    def select(self, value, relative=False, modular=False):
        invLen = len(self.items)
        if relative:
            value += self.selector
        if modular and invLen:
            value %= invLen
        if value < 0:
            value = 0
        if value >= invLen:
            value = invLen-1
        if value in range(invLen):
            self.doSelect(value)
    
    def doSelect(self, value):
        self.selector = value
        self.widget.select(value)
    
    def setItems(self, items):
        self.items = items
        self.selector = utils.clamp(self.selector, 0, len(items)-1)
        self.widget.set_items([self.itemName(item) for item in self.items])
        self.widget.select(self.selector)
    
    def getItem(self, num):
        return self.items[num]
    
    def getSelectedItem(self):
        return self.getItem(self.getSelected())
    
    def getNumItems(self):
        return len(self.items)
    
    def itemName(self, item):
        return item
    
