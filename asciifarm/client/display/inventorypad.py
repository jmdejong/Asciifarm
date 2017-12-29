
import curses
from .selector import Selector

class InventoryPad:
    
    def __init__(self, title):
        self.title = title
        self.selector = Selector(self)
        self.setInventory([])
        self.changed = False
        self.win = None
    
    def setWin(self, win):
        self.win = win
    
    def getSelector(self):
        return self.selector
    
    def change(self):
        self.changed = True
    
    def setInventory(self, items):
        self.items = items
        self.changed = True
    
    def getNumItems(self):
        return len(self.items)
    
    def update(self, force):
        if not self.changed and not force or not self.win:
            return
        win = self.win
        self.changed = False
        height, width = win.getmaxyx()
        win.erase()
        win.addstr(0,0, (self.title + ":")[:width])
        for i, item in enumerate(self.items[:height-1]):
            if i == self.selector.getValue():
                win.addstr(i+1, 0, '*')
            win.addstr(i+1, 1, item)
        win.noutrefresh()
