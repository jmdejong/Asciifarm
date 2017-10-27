#!/usr/bin/python3

import curses

def main(stdscr):
    #curses.start_color()
    curses.use_default_colors()
    for i in range(0, min(256, curses.COLOR_PAIRS, curses.COLORS)):
        curses.init_pair(i, i, -1)
    for i in range(0, min(256, curses.COLOR_PAIRS, curses.COLORS)):
        stdscr.addstr((' %3d' if i % 16 else '\n%3d')%(i), curses.color_pair(i))
    stdscr.addstr("\nCOLORS: {}, COLOR_PAIRS: {}".format(curses.COLORS, curses.COLOR_PAIRS))
    stdscr.addstr("\nPress any key to quit\n")
    stdscr.getch()

curses.wrapper(main)
