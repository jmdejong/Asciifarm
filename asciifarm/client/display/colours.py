
import curses

class Colours:
    
    def __init__(self):
        
        self.colours = min(curses.COLORS, 16)
        self.pairs = self.colours*self.colours

        curses.use_default_colors()
        for i in range(0, self.pairs):
            curses.init_pair(i, i%self.colours, i//self.colours)
    
    def get(self, fg=0, bg=0):
        dfg = fg % self.colours
        dbg = bg % self.colours
        if (dfg, dbg) == (0, 0) and (fg, bg) != (0, 0):
            # avoid unintended use of (0,0), which is settings dependent
            dfg, dbg = 7, 0
        return curses.color_pair(dfg + dbg*self.colours)
