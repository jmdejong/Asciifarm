#!/usr/bin/python3

import curses

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(True)
curses.noecho()

key = stdscr.getch()
keyname = str(curses.keyname(key), "utf-8")


stdscr.addstr(2, 0, keyname)

curses.nocbreak()
stdscr.keypad(True)
curses.echo()
curses.endwin()

print(keyname)
