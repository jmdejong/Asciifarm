
import curses
import textwrap

class MessagePad():
    
    def __init__(self):
        self.changed = False
        self.messages = []
    
    def addMessage(self, message):
        self.messages.append(message)
        self.changed = True
    
    def update(self, win, force):
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
