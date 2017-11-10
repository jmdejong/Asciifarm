
import curses



class InfoPad:
    
    
    
    def __init__(self, size=(1,1), *args):
        self.pad = curses.newpad(size[1], size[0])
        self.size = size
        self.changed = False
        self.lastView = None
    
    def showString(self, string):
        self.pad.clear()
        self.pad.addstr(0,0,string)
        self.changed = True
    
    def update(self, screen, x, y, xmax, ymax, force=False):
        if not self.changed and (x, y, xmax, ymax) == self.lastView or xmax <= x or ymax <= y and not force:
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
