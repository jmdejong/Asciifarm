
import curses
import textwrap

class MessagePad():
    
    def __init__(self):
        self.changed = False
        self.messages = []
        self.widget = None
    
    def setWidget(self, widget):
        self.widget = widget
    
    def addMessage(self, message):
        self.messages.append(message)
        self.widget.change()
    
    def update(self):
        win = self.widget.getWin()
        width, height = win.getSize()
        if height < 1:
            return
        lines = []
        for message in self.messages:
            lines += textwrap.wrap(message, width)
        if len(lines) > height:
            lines = lines[len(lines)-height:]
        win.erase()
        win.addLine((0,0),'\n'.join(lines))
        win.noutrefresh()
