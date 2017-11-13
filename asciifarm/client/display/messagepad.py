
import curses
import textwrap

class MessagePad():
    
    def __init__(self, maxLines=10):
        #self.maxLines = maxLines
        #self.pad = curses.newpad(maxLines+2, 200)
        self.changed = False
        #self.lastView = None
        self.messages = []
    
    def addMessage(self, message):
        self.messages.append(message)
        self.changed = True
    
    #def getHeight(self):
        #return self.maxLines
    
    def update(self, win, force=False):
        if not self.changed and not force or not win:
            return
        height, width = win.getmaxyx()
        if height < 1:
            return
        lines = []
        for message in self.messages:
            lines += textwrap.wrap(message, width)
        if len(lines) > height:
            lines = lines[len(lines)-height:]
        win.erase()
        win.addstr(0,0,'\n'.join(lines))
        self.changed = False
        win.noutrefresh()
            #0,
            #0,
            #y,
            #x,
            #ymax-1,
            #xmax-1)
