
import curses
import json
import os
import getpass
import sys
from .connection import Connection
from .client import Client

defaultAdresses = {
    "abstract": "asciifarm",
    "unix": "asciifarm.socket",
    "inet": "localhost:9021",
    }

def main(name, socketType, address, keybindings, characters):
    
    connection = Connection(socketType)
    try:
        connection.connect(address)
    except ConnectionRefusedError:
        print("ERROR: Could not connect to server.\nAre you sure that the server is running and that you're connecting to the right address?", file=sys.stderr)
        return
    
    caught_ctrl_c = False
    def start(stdscr):
        nonlocal caught_ctrl_c
        try:
            client = Client(stdscr, name, connection, keybindings, characters)
        except KeyboardInterrupt:
            caught_ctrl_c = True
    
    curses.wrapper(start)
    
    if caught_ctrl_c:
        print('^C caught, goodbye!')
