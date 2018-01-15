
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
    
    def setTitle(self, title):
        self.title = title
    
    def getNumItems(self):
        return len(self.items)
    
    def update(self):
        win = self.widget.getWin()
        width, height = win.getSize()
        height -= 1
        selected = self.selector.getValue()
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
