
from client import Client
from connection import Connection
import curses
import json
import os

def main(name, address, keybindingsFile=None, characterFile=None):
    
    if keybindingsFile == None:
        fname = os.path.join(os.path.dirname(__file__), "keybindings.json")
        keybindingsFile = open(fname)
    keybindings = json.load(keybindingsFile)
    keybindingsFile.close()
    
    if characterFile == None:
        fname = os.path.join(os.path.dirname(__file__), "characters.json")
        characterFile = open(fname)
    characters = json.load(characterFile)
    characterFile.close()
    
    connection = Connection()
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
