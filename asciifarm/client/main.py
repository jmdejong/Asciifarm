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
    
    def start(stdscr):
        display = Display(stdscr, characters, colours)
        client = Client(stdscr, display, name, connection, keybindings, logfile)
        try:
            client.start()
        except KeyboardInterrupt:
            client.close("^C caught, goodbye")
        except Exception as e:
            # throw the execption outside ncurses
            # so the cleanup can happen first
            nonlocal error
            error = e
        nonlocal closeMessage
        closeMessage = client.closeMessage

    curses.wrapper(start)
    
    if error is not None:
        raise error
    
    if closeMessage:
        print(closeMessage, file=sys.stderr)

