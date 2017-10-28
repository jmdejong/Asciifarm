#!/usr/bin/python3

import curses

def main(stdscr):
    #curses.start_color()
    curses.use_default_colors()
    colours = min(curses.COLORS, 16)
    for y in range(0, colours):
        for x in range(0, colours):
            i = x+y*colours
            curses.init_pair(i, x, y)
            stdscr.addstr((' '  if x else '\n') + "%2d,%2d"%(x, y), curses.color_pair(i))
    stdscr.addstr("\n\nPress any key to quit\n")
    stdscr.getch()

curses.wrapper(main)
