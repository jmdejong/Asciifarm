
import curses

class Colours:
    
    def __init__(self):
        
        self.colours = min(curses.COLORS, 16)
        self.pairs = self.colours*self.colours

        curses.use_default_colors()
        for i in range(0, self.pairs):
            curses.init_pair(i, i%self.colours, i//self.colours)
    
    def get(self, fg=0, bg=0):
        fg %= self.colours
        bg %= self.colours
        return curses.color_pair(fg + bg*self.colours)
