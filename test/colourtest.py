#!/usr/bin/python3

import curses

def main(stdscr):
    #curses.start_color()
    curses.use_default_colors()
    for i in range(0, min(256, curses.COLOR_PAIRS)):
        curses.init_pair(i, i%16, i//16)
    try:
        for i in range(0, min(256, curses.COLOR_PAIRS)):
            stdscr.addstr((' %3d' if i % 16 else '\n%3d')%(i), curses.color_pair(i))
        stdscr.addstr("\n\nPress any key to quit\n")
    except curses.ERR:
        # End of screen reached
        pass
    stdscr.getch()

curses.wrapper(main)
