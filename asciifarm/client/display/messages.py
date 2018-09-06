
import textwrap

from .widimp import WidImp

class Messages(WidImp):
    
    def __init__(self):
        self.changed = False
        self.messages = []
        self.scrolledBack = 0
    
    def addMessage(self, message):
        self.messages.append(message)
        if self.scrolledBack:
            self.scrolledBack += 1
        self.change()
    
    def scroll(self, amount, relative=True):
        if relative:
            self.scrolledBack += amount
        else:
            self.scrolledBack = amount
        self.scrolledBack = max(self.scrolledBack, 0)
        self.change()
    
    def update(self, win):
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
