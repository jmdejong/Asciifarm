
import curses

class InventoryPad:
    
    def __init__(self, title, maxItems=20):
        self.title = title
        #self.maxItems = maxItems
        #self.pad = curses.newpad(maxItems+2, 100)
        self.setInventory([])
        self.changed = False
        #self.lastView = None
    
    def setInventory(self, items):
        self.items = items
        #self.pad.erase()
        #self.pad.addstr(0,0, self.title + ":\n")
        #for i, item in enumerate(items[:self.maxItems]):
            #self.pad.addstr(i+1, 2, item)
        self.changed = True
    
    def getHeight(self):
        return self.maxItems+2
    
    def update(self, win, force=False):
        if not self.changed and not force or not win:
            return
        #self.lastView = (x, y, xmax, ymax)
        self.changed = False
        height, width = win.getmaxyx()
        win.erase()
        win.addstr(0,0, (self.title + ":")[:width])
        for i, item in enumerate(self.items[:height-1]):
            win.addstr(i+1, 2, item)
        win.noutrefresh()
            #0,
            #0,
            #y,
            #x,
            #ymax-1,
            #xmax-1)
