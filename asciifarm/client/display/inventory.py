
from asciifarm.common import utils

from .widimp import WidImp

class Inventory(WidImp):
    
    def __init__(self, title):
        self.title = title
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
            self.selector = value
            self.change()
    
    def setInventory(self, items):
        self.items = items
        self.selector = utils.clamp(self.selector, 0, len(items)-1)
        self.change()
    
    def setTitle(self, title):
        self.title = title
    
    def getNumItems(self):
        return len(self.items)
    
    def update(self, win):
        width, height = win.getSize()
        height -= 1
        selected = self.selector
        start = min(selected - height//2, len(self.items)-height)
        start = max(start, 0)
        end = start + height
        win.erase()
        win.addLine((0,0), (self.title + ":")[:width])
        for i, item in enumerate(self.items[start:end]):
            if i + start == selected:
                win.addLine((0, i+1), '*')
            win.addLine((1, i+1), item)
        if end < len(self.items):
            win.addLine((width-1, height), "+")
        if start > 0:
            win.addLine((width-1, 1), "-")
        win.noutrefresh()
