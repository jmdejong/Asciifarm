
import curses
import textwrap

class MessagePad:
    
    def __init__(self, maxLines=10):
        self.maxLines = maxLines
        self.pad = curses.newpad(maxLines+2, 200)
        self.changed = False
        self.lastView = None
        self.messages = []
    
    def addMessage(self, message):
        self.messages.append(message)
        self.changed = True
    
    def getHeight(self):
        return min(len(self.messages), self.maxLines)
    
    def update(self, screen, x, y, xmax, ymax):
        if not self.changed and (x, y, xmax, ymax) == self.lastView :
            return
        width = xmax - x
        height = ymax - y # should equal self.getHeight()
        if height < 1:
            return
        lines = []
        for message in self.messages:
            lines += textwrap.wrap(message, width)
        if len(lines) > height:
            lines = lines[len(lines)-height:]
        self.pad.erase()
        self.pad.addstr(0,0,'\n'.join(lines))
        self.changed = False
        self.pad.noutrefresh(
            0,
            0,
            y,
            x,
            ymax-1,
            xmax-1)
