
import curses


class FieldPad:
    
    
    def __init__(self, size=(1,1), charSize=1, colours=False):
        self.pad = curses.newpad(size[1]+1, (size[0]+1)*charSize)
        self.size = size
        self.charSize = charSize
        self.center = (0, 0)
        self.colours = colours
        self.changed = False
        self.widget = None
    
    def setWidget(self, widget):
        self.widget = widget
    
    def resize(self, width, height):
        self.size = (width, height)
        self.pad.resize(height+1, width*self.charSize)
        self.widget.change()
        win = self.widget.getWin()
        if win:
            win.erase()
            win.noutrefresh()
    
    def changeCell(self, x, y, sprites):
        """ sprites must always have at least one element """
        char, colour, bgcolour = sprites[0]
        if bgcolour == None:
            for (ch, co, bg) in sprites:
                if bg != None:
                    bgcolour = bg
                    break
            else:
                bgcolour = 0
        if colour != None and self.colours:
            self.pad.addstr(y, x*self.charSize, char, self.colours.get(colour, bgcolour))
        else:
            self.pad.addstr(y, x*self.charSize, char)
        self.widget.change()
    
    def setCenter(self, pos):
        self.center = pos
        self.widget.change()
    
    def getWidth(self):
        return self.size[0]*self.charSize
    
    def getHeight(self):
        return self.size[1]
    
    def _roundWidth(self, x):
        return x // self.charSize * self.charSize
    
    def update(self):
        win = self.widget.getWin()
        width, height = win.getSize()
        x, y = win.getPos()
        xmax = x + width
        ymax = y + height
        self.pad.noutrefresh(
            max(0, min(self.getHeight()-height, self.center[1] - int(height/2))),
            max(0, min(
                self._roundWidth(self.getWidth()-width),
                self._roundWidth(self.center[0]*self.charSize - int(width/2)))),
            y,
            x + max(0, (width - self.getWidth()) // 2),
            ymax,
            xmax)
