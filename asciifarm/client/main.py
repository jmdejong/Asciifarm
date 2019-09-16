#! /usr/bin/python3
import curses
import json
import os
import getpass
import sys
from .connection import Connection
from .gameclient import Client
from .display.display import Display
from .parseargs import parse_args

def main(argv=None):
    
    (name, socketType, address, keybindings, characters, colours, logfile) = parse_args(argv)
    
    
    connection = Connection(socketType)
    try:
        connection.connect(address)
    except ConnectionRefusedError:
        print("ERROR: Could not connect to server.\nAre you sure that the server is running and that you're connecting to the right address?", file=sys.stderr)
        return
    
    error = None
    closeMessage = None
    
    os.environ.setdefault("ESCDELAY", "25")
    
    try:
        # Initialize curses
        stdscr = curses.initscr()

        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        curses.noecho()
        curses.cbreak()

        # In keypad mode, escape sequences for special keys
        # (like the cursor keys) will be interpreted and
        # a special value like curses.KEY_LEFT will be returned
        stdscr.keypad(1)

        # Start color, too.  Harmless if the terminal doesn't have
        # color; user can test with has_color() later on.  The try/catch
        # works around a minor bit of over-conscientiousness in the curses
        # module -- the error return from C start_color() is ignorable.
        try:
            curses.start_color()
        except:
            pass

        display = Display(stdscr, characters, colours)
        client = Client(stdscr, display, name, connection, keybindings, logfile)
        try:
            client.start()
        except KeyboardInterrupt:
            client.close("^C caught, goodbye")
        except Exception as e:
            # throw the execption outside ncurses
            # so the cleanup can happen first
            error = e
        closeMessage = client.closeMessage
    finally:
        # Set everything back to normal
        if 'stdscr' in locals():
            stdscr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
        
    
    if error is not None:
        raise error
    
    if closeMessage:
        print(closeMessage, file=sys.stderr)

