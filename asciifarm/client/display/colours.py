
import curses

class Colours:
    
    def __init__(self):
        
        self.colours = min(curses.COLORS, 16)
        self.pairs = self.colours*self.colours

        curses.use_default_colors()
        for i in range(0, self.pairs):
            curses.init_pair(i, i%self.colours, i//self.colours)
    
    def get(self, fg=0, bg=0):
        if self.colours == 16:
            return curses.color_pair(fg + bg*self.colours)
        elif self.colours == 8:
            dfg = fg % 8
            dbg = bg % 8
            if bg == 8:
                dbg = 7
            if fg == 8:
                dfg = 7
            colour = curses.color_pair(dfg + dbg*self.colours)
            if fg >= 8 and bg < 8:
                colour |= curses.A_BOLD
            elif fg < 8 and bg >= 8:
                colour |= curses.A_DIM
            return colour
        else:
            return curses.color_pair(0)
