
import curses
import textwrap

class MessagePad():
    
    def __init__(self):
        self.changed = False
        self.messages = []
        self.widget = None
        self.scrolledBack = 0
    
    def setWidget(self, widget):
        self.widget = widget
    
    def addMessage(self, message):
        self.messages.append(message)
        if self.scrolledBack:
            self.scrolledBack += 1
        self.widget.change()
    
    def scroll(self, amount, relative=True):
        if relative:
            self.scrolledBack += amount
        else:
            self.scrolledBack = amount
        self.scrolledBack = max(self.scrolledBack, 0)
        self.widget.update()
        self.widget.doUpdate()
    
    def update(self):
        win = self.widget.getWin()
        width, height = win.getSize()
        if height < 1:
            return
        lines = []
        messages = self.messages
        for message in messages:
            lines += textwrap.wrap(message, width)
        self.scrolledBack = max(min(self.scrolledBack, len(lines)-height), 0)
        moreDown = False
        if self.scrolledBack > 0:
            lines = lines[:-self.scrolledBack]
            moreDown = True
        moreUp = False
        if len(lines) > height:
            moreUp = True
            lines = lines[len(lines)-height:]
        elif len(lines) < height:
            lines = (height-len(lines)) * [""] + lines
        win.erase()
        for i, line in enumerate(lines):
            win.addLine((0,i),line)
        if moreUp:
            win.addLine((width-1, 0), '-')
        if moreDown:
            win.addLine((width-1, height-1), '+')
        win.noutrefresh()
