
import curses
from .selector import Selector

class InventoryPad:
    
    def __init__(self, title):
        self.title = title
        self.selector = Selector(self)
        self.widget = None
        self.items = []
    
    def setWidget(self, widget):
        self.widget = widget
    
    def getSelector(self):
        return self.selector
    
    def change(self):
        self.widget.change()
    
    def setInventory(self, items):
        self.items = items
        self.widget.change()
    
    def getNumItems(self):
        return len(self.items)
    
    def update(self):
        win = self.widget.getWin()
        height, width = win.getmaxyx()
        win.erase()
        win.addstr(0,0, (self.title + ":")[:width])
        for i, item in enumerate(self.items[:height-1]):
            if i == self.selector.getValue():
                win.addstr(i+1, 0, '*')
            win.addstr(i+1, 1, item)
        win.noutrefresh()
