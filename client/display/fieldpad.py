
import curses


class FieldPad:
    
    
    
    def __init__(self, size=(1,1), charSize=1, *args):
        self.pad = curses.newpad(size[1]+1, (size[0]+1)*charSize)
        self.size = size
        self.charSize = charSize
        self.center = (0, 0)
    
    def resize(self, width, height):
        self.size = (width, height)
        self.pad.resize(height+1, width*self.charSize1)
    
    def changeCell(self, x, y, char):
        self.pad.addstr(y, x*self.charSize, char)
    
    def setCenter(self, pos):
        self.center = pos
    
    def getWidth(self):
        return self.size[0]*self.charSize
    
    def getHeight(self):
        return self.size[1]
    
    def update(self, screen, x, y, xmax, ymax):
        width = xmax-x
        height = ymax-y
        self.pad.noutrefresh(
            min(self.getHeight()-height, max(0, self.center[1] - int(height/2))),
            min(self.getWidth()-width, max(0, self.center[0]*self.charSize - int(width/2))),
            y,
            x,
            ymax-1,
            xmax-1)
