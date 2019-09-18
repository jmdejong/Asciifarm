#! /usr/bin/python3

import json

import sys
import termios
import tty
import signal
#import os

from .connection import Connection
from .gameclient import Client
from .newdisplay.display import Display
from .parseargs import parse_args
from ratuil.screen import Screen

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
    
    #os.environ.setdefault("ESCDELAY", "25")
    
    fd = sys.stdin.fileno()
    oldterm = termios.tcgetattr(fd)
    
    try:
        
        tty.setraw(sys.stdin)
        Screen.default.hide_cursor()

        display = Display(characters)
        client = Client(display, name, connection, keybindings, logfile)
        signal.signal(signal.SIGWINCH, client.onSigwinch)
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
        ## Set everything back to normal
        termios.tcsetattr(fd, termios.TCSADRAIN, oldterm)
        Screen.default.finalize()
        
    
    if error is not None:
        raise error
    
    if closeMessage:
        print(closeMessage, file=sys.stderr)

