
import curses

class TextInput:
    
    def __init__(self):
        self.widget = None
        self.text = ""
        self.cursor = 0
    
    def setWidget(self, widget):
        self.widget = widget
    
    def setText(self, text, cursor):
        self.text = text
        self.cursor = cursor
        self.widget.change()
    
    def update(self, win):
        width, height = win.getSize()
        win.erase()
        win.addLine((0, 0), self.text[:width])
        if self.cursor >= 0 and self.cursor <= len(self.text):
            win.setAttr((min(self.cursor, width-1), 0), curses.A_REVERSE)
        win.noutrefresh()
