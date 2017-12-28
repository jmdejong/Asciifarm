
import curses
import textwrap

class MessagePad():
    
    def __init__(self):
        self.changed = False
        self.messages = []
        self.win = None
    
    def setWin(self, win):
        self.win = win
    
    def addMessage(self, message):
        self.messages.append(message)
        self.changed = True
    
    def update(self, force):
        if not self.changed and not force or not self.win:
            return
        win = self.win
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
