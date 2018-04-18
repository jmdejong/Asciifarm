
import curses

class Window:
    """ Small wrapper around curses windows """
    
    def __init__(self, win, colours=None):
        
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
        y, x = self.win.getparyx()
        return (x, y)
    
    def addLine(self, pos, string, colour=(0,0)):
        """Draw a string that does not contain newlines or characters with larger width
        
        long lines are cropped to fit in the window"""
        x, y = pos
        width, height = self.getSize()
        string = string[:width-x]
        drawLast = None
        if self.colours:
            self._addstr(y, x, string, self.colours.get(*colour))
        else:
            self._addstr(y, x, string)

    
    def _addstr(self, y, x, string, *args):
        width, height = self.getSize()
        if y == height-1 and x+len(string) == width:
            if len(string) > 1:
                self.win.addstr(y, x, string[:-1], *args)
            try:
                self.win.addstr(height-1, width-1, string[-1], *args)
            except curses.error:
                # ncurses has a weird problem:
                # it always raises an error when drawing to the last character in the window
                # it draws first and then raises the error
                # therefore to draw in the last place of the window the last character needs to be ingored
                # other solutions might be possible, but are more hacky
                pass
        else:
            self.win.addstr(y, x, string, *args)
    
    def erase(self):
        self.win.erase()
    
    def noutrefresh(self):
        self.win.noutrefresh()
    
    def getStr(self, pos):
        x, y = pos
        return self.win.getstr(y, x)
    
    def getCh(self, pos):
        x, y = pos
        return self.win.getch(y, x)
    
    def setAttr(self, pos, attr, num=1):
        x, y = pos
        self.win.chgat(y, x, num, attr)
    
    
    
