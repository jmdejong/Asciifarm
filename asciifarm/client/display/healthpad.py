
import curses



class HealthPad:
    
    
    
    def __init__(self, size=(1,1), *args):
        self.pad = curses.newpad(size[1], size[0])
        self.size = size
    
    def setHealth(self, health, maxHealth):
        self.pad.erase()
        self.pad.addstr(0,0,"Health: {}/{}".format(health, maxHealth))
    
    def update(self, screen, x, y, xmax, ymax):
        self.pad.noutrefresh(
            0,
            0,
            y,
            x,
            ymax-1,
            xmax-1)
