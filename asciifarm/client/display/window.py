


class Window:
    """ Small wrapper around curses windows """
    
    def __init__(self, win, colours=False):
        
        self.setWin(win)
        self.colours = colours
            
    
    
    def setWin(self, win):
        self.win = win
    
    def getSize(self):
        if not self.win:
            return (0, 0)
        height, width = self.win.getmaxyx()
        return (width, height)
    
    def getPos(self):
        if not self.win:
            return (0, 0)
        y, x = win.getparyx()
        return (x, y)
    
    def addString(self, pos, string, colour=(0,0)):
        x, y = pos
        if self.colours:
            self.win.addstr(y, x, string, self.colours.get(colour))
        else:
            self.win.addstr(y, x, string)
    
    def erase(self):
        self.win.erase()
    
    
    
