
import curses

class InventoryPad:
    
    def __init__(self, title):
        self.title = title
        self.setInventory([])
        self.changed = False
    
    def setInventory(self, items):
        self.items = items
        self.changed = True
    
    def getHeight(self):
        return self.maxItems+2
    
    def update(self, win, force):
        if not self.changed and not force or not win:
            return
        self.changed = False
        height, width = win.getmaxyx()
        win.erase()
        win.addstr(0,0, (self.title + ":")[:width])
        for i, item in enumerate(self.items[:height-1]):
            win.addstr(i+1, 2, item)
        win.noutrefresh()
