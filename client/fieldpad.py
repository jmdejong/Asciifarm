
import curses


class FieldPad:
    
    
    
    def __init__(self, size=(1,1), charSize=1, *args):
        self.pad = curses.newpad(size[1]+1, size[0]*charSize+1)
        self.size = size
        self.charSize = charSize
    
    def resize(self, width, height):
        self.size = (width, height)
        self.pad.resize(height+1, width*self.charSize1)
    
    def changeCell(self, x, y, char):
        self.pad.addstr(y, x*self.charSize, char)
    
    def getWidth(self):
        return self.size[0]
    
    def getHeight(self):
        return self.size[1]
    
    def update(self, screen, x, y, xmax, ymax):
        self.pad.noutrefresh(
            0,
            0,
            y,
            x,
            ymax,
            xmax)
