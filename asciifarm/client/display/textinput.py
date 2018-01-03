
import curses

class TextInput:
    
    def __init__(self):
        self.reading = False
        self.widget = None
    
    def setWidget(self, widget):
        self.widget = widget
    
    def getString(self):
        win = self.widget.getWin()
        if not win:
            return None
        self.reading = True
        curses.echo()
        curses.nocbreak()
        win.addLine((0, 0), ">")
        string = win.getStr((2,0))
        curses.noecho()
        curses.cbreak()
        self.reading = False
        win.erase()
        win.noutrefresh()
        self.widget.doUpdate()
        return string
    
    def update(self):
        pass
