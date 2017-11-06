
import curses

class InventoryPad:
    
    def __init__(self, title, maxItems=20):
        self.title = title
        self.maxItems = maxItems
        self.pad = curses.newpad(maxItems+2, 100)
        self.setInventory([])
        self.changed = False
        self.lastView = None
    
    def setInventory(self, items):
        self.items = items
        self.pad.erase()
        self.pad.addstr(0,0, self.title + ":\n")
        for i, item in enumerate(items[:self.maxItems]):
            self.pad.addstr(i+1, 2, item)
        self.changed = True
    
    def getHeight(self):
        return self.maxItems+2
    
    def update(self, screen, x, y, xmax, ymax):
        if not self.changed and (x, y, xmax, ymax) == self.lastView or xmax <= x or ymax <= y:
            return
        self.lastView = (x, y, xmax, ymax)
        self.changed = False
        self.pad.noutrefresh(
            0,
            0,
            y,
            x,
            ymax-1,
            xmax-1)
