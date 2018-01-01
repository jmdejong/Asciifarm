
import curses
from .selector import Selector

class InventoryPad:
    
    def __init__(self, title):
        self.title = title
        self.selector = Selector(self)
        self.widget = None
        self.items = []
    
    def setWidget(self, widget):
        self.widget = widget
    
    def getSelector(self):
        return self.selector
    
    def change(self):
        self.widget.change()
    
    def setInventory(self, items):
        self.items = items
        self.widget.change()
    
    def getNumItems(self):
        return len(self.items)
    
    def update(self):
        win = self.widget.getWin()
        height, width = win.getmaxyx()
        height -= 1
        selected = self.selector.getValue()
        start = min(selected - height//2, len(self.items)-height)
        start = max(start, 0)
        end = start + height
        win.erase()
        win.addstr(0,0, (self.title + ":")[:width])
        for i, item in enumerate(self.items[start:end]):
            if i + start == selected:
                win.addstr(i+1, 0, '*')
            win.addstr(i+1, 1, item)
        if end < len(self.items):
            try:
                win.addstr(height, width-1, "+")
            except curses.error:
                # ncurses has a weird problem:
                # it always raises an error when drawing to the last character in the window
                # it draws first and then raises the error
                # therefore to draw in the last place of the window the last character needs to be ingored
                # other solutions might be possible, but are more hacky
                pass
        if start > 0:
            win.addstr(1, width-1, "-")
        win.noutrefresh()
