
import curses
import json
import os
import getpass
import sys
from .connection import Connection
from .gameclient import Client
from .display.display import Display

defaultAdresses = {
    "abstract": "asciifarm",
    "unix": "asciifarm.socket",
    "inet": "localhost:9021",
    }

def main(name, socketType, address, keybindings, characters, colours=False, logfile=None):
    
    connection = Connection(socketType)
    try:
        connection.connect(address)
    except ConnectionRefusedError:
        print("ERROR: Could not connect to server.\nAre you sure that the server is running and that you're connecting to the right address?", file=sys.stderr)
        return
    
    closeMessage = None
    
    os.environ.setdefault("ESCDELAY", "25")
    
    def start(stdscr):
        display = Display(stdscr, characters, colours)
        client = Client(stdscr, display, name, connection, keybindings, logfile)
        try:
            client.start()
        except KeyboardInterrupt:
            client.close("^C caught, goodbye")
        nonlocal closeMessage
        closeMessage = client.closeMessage
    
    curses.wrapper(start)
    
    if closeMessage:
        print(closeMessage, file=sys.stderr)
